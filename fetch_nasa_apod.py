import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlsplit, unquote
from helpers import download_image, get_file_extension
import argparse


def fetch_nasa_apod(count, api_key):
    url = "https://api.nasa.gov/planetary/apod"
    params = {
        'api_key': api_key,
        'count': count
    }
    response = requests.get(url, params=params)
    response.raise_for_status()
    apod_data = response.json()
    images_dir = Path("nasa_images")
    images_dir.mkdir(parents=True, exist_ok=True)
    for index, item in enumerate(apod_data, start=1):
        if item['media_type'] != 'image':
            continue

        image_url = item['url']
        extension = get_file_extension(image_url)
        filename = f"nasa_{index}{extension}"
        file_path = images_dir / filename
        download_image(image_url, file_path)


def main():
    load_dotenv()
    api_key = os.getenv("API_KEY_NASA")
    parser = argparse.ArgumentParser(
        description='Скачивание Astronomy Picture of the Day от NASA'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=30,
        help='Количество фото для скачивания (по умолчанию: 30)',
        choices=range(1, 51)
    )
    args = parser.parse_args()
    fetch_nasa_apod(args.count, api_key)


if __name__ == "__main__":
    main()
