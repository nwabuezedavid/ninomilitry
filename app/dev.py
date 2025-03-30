import openai
import os
import base64
from io import BytesIO
from django.utils.text import slugify
from django.utils import timezone
from .models import *
from django.contrib.auth.models import User

# OpenAI API Key
openai.api_key = "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"

def generate_blog_from_image(image_path, user_id):
    """ Generate a blog post from an image using OpenAI GPT-4 Vision """
    try:
        # Read the image and convert to Base64
        with open(image_path, "rb") as img_file:
            base64_image = base64.b64encode(img_file.read()).decode("utf-8")

        # Send to OpenAI for analysis
        response = openai.ChatCompletion.create(
            model="gpt-4-vision-preview",
            messages=[
                {"role": "system", "content": "You are an AI that writes professional blog posts based on images."},
                {"role": "user", "content": [
                    {"type": "text", "text": "Analyze this image and create a detailed blog post about it."},
                    {"type": "image_url", "image_url": f"data:image/jpeg;base64,{base64_image}"}
                ]}
            ]
        )

        # Extract response
        blog_content = response['choices'][0]['message']['content']

        # Generate a title from the first line
        title = blog_content.split("\n")[0].strip()
        slug = slugify(title)

        # Get the user who is creating the post
        author = User.objects.get(id=user_id)

        # Save to BlogPost model
        blog_post = BlogPost.objects.create(
            title=title,
            slug=slug,
            author=author,
            content=blog_content,
            featured_image=image_path,  # Store image path in the model
            created_date=timezone.now(),
            published_date=timezone.now(),
            updated_date=timezone.now(),
            is_featured=True
        )

        return f"Blog post '{title}' created successfully!"

    except Exception as e:
        return f"Error: {str(e)}"

# Example Usage
# generate_blog_from_image("media/blog_images/military_officer.jpg", user_id=1)
 
# OpenAI API Key

def generate_blog_from_title(title, user_id):
    """ Generate a blog post from a given title using OpenAI GPT-4 """
    try:
        # Request AI-generated blog content
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional blog writer."},
                {"role": "user", "content": f"Write a detailed blog post about: {title}"}
            ]
        )

        # Extract generated content
        blog_content = response['choices'][0]['message']['content']
        slug = slugify(title)

        # Get the user who is creating the post
        author = User.objects.get(id=user_id)

        # Save to BlogPost model
        blog_post = BlogPost.objects.create(
            title=title,
            slug=slug,
            author=author,
            content=blog_content,
            created_date=timezone.now(),
            published_date=timezone.now(),
            updated_date=timezone.now(),
            is_featured=True
        )

        return f"Blog post '{title}' created successfully!"

    except Exception as e:
        return f"Error: {str(e)}"

# Example Usage
# generate_blog_from_title("The Future of AI in Military Strategy", user_id=1)
