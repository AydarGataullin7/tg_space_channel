import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlsplit, unquote

load_dotenv()
API_KEY = os.getenv("API_KEY_NASA")


def download_image(url, file_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(file_path, "wb") as f:
        f.write(response.content)


def fetch_nasa_epic():
    url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={API_KEY}"
    images_dir = Path("epic_images")
    images_dir.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for i, item in enumerate(data[:10], start=1):
            image_name = item["image"]
            date_str = item["date"]
            date_only = date_str.split()[0]
            year, month, day = date_only.split("-")
            epic_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png?api_key={API_KEY}"
            filename = (f"epic_{i}.png")
            file_path = images_dir / filename
            download_image(epic_url, file_path)

    except Exception as e:
        print(f"Ошибка при получении данных от NASA: {e}")


def fetch_spacex_last_launch():
    url = 'https://api.spacexdata.com/v5/launches/5eb87d47ffd86e000604b38a'
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    images_url = data['links']['flickr']['original']
    images_dir = Path("spacex_images")
    images_dir.mkdir(parents=True, exist_ok=True)

    for index, images in enumerate(images_url, start=1):
        filename = (f"spacex_{index}.jpg")
        file_path = images_dir / filename
        download_image(images, file_path)


def fetch_nasa_apod():
    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&count=30"
    response = requests.get(url)
    response.raise_for_status()
    data = response.json()
    images_dir = Path("nasa_images")
    images_dir.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(data, start=1):
        if item['media_type'] == 'image':
            image_url = item['url']
            extension = get_file_extension(image_url)
            filename = (f"nasa_{index}{extension}")
            file_path = images_dir / filename
            download_image(image_url, file_path)


def get_file_extension(url):
    url_file = urlsplit(url)
    path_of_url = url_file.path
    decoded_path = unquote(path_of_url)
    file_name = os.path.split(decoded_path)[1]
    extension = os.path.splitext(file_name)[1]
    return extension


def main():
    fetch_nasa_epic()
    fetch_nasa_apod()
    fetch_spacex_last_launch()


if __name__ == "__main__":
    main()
