ss = '44a6c530e258446b8ac1a484816a6ba3'  # Replace with your News API key
import random
import requests
from django.utils.text import slugify
from django.utils import timezone
from newsapi import NewsApiClient
from .models import BlogPost
from django.contrib.auth.models import User

# API Keys
NEWS_API_KEY = "44a6c530e258446b8ac1a484816a6ba3"  # Replace with your News API Key
PEXELS_API_KEY = "EdTUeQZfE2vteymon62P1uK6uizxyb7tr8QfYdRoOMqBHUuhTpWK869R"  # Replace with your Pexels API Key

def get_random_military_officer_image():
    """Fetch a random military officer image from Pexels"""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": "military officer", "per_page": 10}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if data["photos"]:
            image = random.choice(data["photos"])  # Pick a random image
            return image["src"]["medium"]  # Return the image URL
    return None  # Return None if no image is found

def fetch_and_save_military_news():
    """Fetch military news and save articles with random military images"""
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    articles = newsapi.get_everything(q='military', language='en', sort_by='publishedAt', page_size=10)

    selected_articles = random.sample(articles['articles'], min(len(articles['articles']), 5))

    # Get or create a default author
    author, created = User.objects.get_or_create(username='news_bot', defaults={'email': 'news_bot@example.com'})

    saved_articles = []
    for article in selected_articles:
        title = article['title']
        slug = slugify(title)
        content = article['description'] or ''
        source_url = article['url']
        published_date = article['publishedAt']
        image_url = article['urlToImage'] # Get a random image

        # Check if the article already exists
        if not BlogPost.objects.filter(slug=slug).exists():
            blog_post = BlogPost(
                title=title,
                slug=slug,
                author=User.objects.get(username='admin'),
                content=content,
                created_date=timezone.now(),
                published_date=published_date,
                url=image_url  # Assigning the image URL
            )
            blog_post.save()
            saved_articles.append(blog_post)

    return saved_articles  # Returns list of saved articles
