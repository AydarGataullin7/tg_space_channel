import requests
import os
from pathlib import Path
from dotenv import load_dotenv
from urllib.parse import urlsplit, unquote
from helpers import download_image
import argparse


def fetch_nasa_epic(count, API_KEY):
    url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={API_KEY}"
    images_dir = Path("epic_images")
    images_dir.mkdir(parents=True, exist_ok=True)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        for i, item in enumerate(data[:count], start=1):
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


def main():
    load_dotenv()
    API_KEY = os.getenv("API_KEY_NASA")
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
    fetch_nasa_epic(args.count, API_KEY)


if __name__ == "__main__":
    main()
