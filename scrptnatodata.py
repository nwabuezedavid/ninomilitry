import requests
from bs4 import BeautifulSoup

def scrape_nato_photos():
    url = "https://www.nato.int/cps/en/natohq/photos.htm"
    base_url = "https://www.nato.int"
    
    response = requests.get(url)
    
    if response.status_code != 200:
        return {"error": "Failed to fetch page"}
    
    soup = BeautifulSoup(response.text, "html.parser")
    
    photo_data = []
    
    # Find all divs with class "inner"
    for div in soup.find_all("div", class_="inner"):
        title_tag = div.find("strong", class_="title")
        img_tag = div.find("img")

        if title_tag and img_tag:
            title = title_tag.text.strip()
            image_url = base_url + img_tag["src"]  # Append base URL to get full image link
            
            photo_data.append({"title": title, "image_url": image_url})

    return photo_data

# Example usage
photos = scrape_nato_photos()
for photo in photos:
    print(photo["title"], "-", photo["image_url"])
