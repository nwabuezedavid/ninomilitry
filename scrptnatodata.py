import requests
from bs4 import BeautifulSoup

def scrape_nato_photos():
    url = "https://www.nato.int/cps/en/natohq/photos.htm?search_types=Photo%20gallery&display_mode=photo&chunk=2"
    base_url = "https://www.nato.int"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
    }

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("Error:", response.status_code, response.text)  # Debugging
        return {"error": "Failed to fetch page"}

    soup = BeautifulSoup(response.text, "html.parser")

    photo_data = []

    for div in soup.find_all("div", class_="inner"):
        title_tag = div.find("strong", class_="title")
        img_tag = div.find("img")

        if title_tag and img_tag:
            title = title_tag.text.strip()
            image_url = base_url + img_tag["src"]
            photo_data.append({"title": title, "image_url": image_url})

    return photo_data

# Run and print results
photos = scrape_nato_photos()

if isinstance(photos, dict) and "error" in photos:
    print("Error:", photos["error"])
else:
    for photo in photos:
        print(photo["title"], "-", photo["image_url"])
