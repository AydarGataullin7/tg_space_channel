import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlsplit, unquote
from helpers import download_image, get_file_extension
import argparse


def fetch_nasa_apod(count, API_KEY):

    url = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}&count={count}"
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


def main():
    load_dotenv()
    API_KEY = os.getenv("API_KEY_NASA")
    parser = argparse.ArgumentParser()
    parser.add_argument('--count', type=int, default=30)
    args = parser.parse_args()
    fetch_nasa_apod(args.count, API_KEY)


if __name__ == "__main__":
    main()
