import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlsplit, unquote
from helpers import download_image
import argparse


def fetch_nasa_epic(count, api_key):
    url = "https://api.nasa.gov/EPIC/api/natural/images"
    params = {'api_key': api_key}
    images_dir = Path("epic_images")
    images_dir.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        epic_images_data = response.json()
        for i, item in enumerate(epic_images_data[:count], start=1):
            image_name = item["image"]
            date_str = item["date"]
            date_only = date_str.split()[0]
            year, month, day = date_only.split("-")
            epic_url = f"https://api.nasa.gov/EPIC/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
            epic_params = {'api_key': api_key}
            filename = (f"epic_{i}.png")
            file_path = images_dir / filename
            download_image(epic_url, epic_params, file_path)
    except (requests.exceptions.RequestException, IOError) as e:
        print(f"Ошибка при получении данных от NASA: {e}")


def main():
    load_dotenv()
    api_key = os.getenv("API_KEY_NASA")
    parser = argparse.ArgumentParser(
        description='Скачивание снимков Земли от NASA EPIC'
    )
    parser.add_argument(
        '--count',
        type=int,
        default=10,
        help='Количество фото для скачивания (по умолчанию: 10)',
        choices=range(1, 51)
    )
    args = parser.parse_args()
    fetch_nasa_epic(args.count, api_key)


if __name__ == "__main__":
    main()
