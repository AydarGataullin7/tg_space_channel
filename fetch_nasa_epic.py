import requests
import os
import datetime
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
    except (requests.exceptions.RequestException, IOError) as e:
        print(f"Ошибка при получении данных от NASA: {e}")
        return

    for image_index, image_data in enumerate(epic_images_data[:count], start=1):
        image_name = image_data["image"]
        date_str = image_data["date"]
        date_obj = datetime.datetime.fromisoformat(
            date_str.replace("Z", "+00:00"))
        epic_url = f"https://api.nasa.gov/EPIC/archive/natural/{date_obj:%Y/%m/%d}/png/{image_name}.png"
        epic_params = {'api_key': api_key}
        filename = (f"epic_{image_index}.png")
        file_path = images_dir / filename
        download_image(epic_url, epic_params, file_path)


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
