import requests
from pathlib import Path
from urllib.parse import urlsplit, unquote
from helpers import download_image
import argparse


def get_all_launches():
    url = 'https://api.spacexdata.com/v5/launches'
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def get_last_launch_with_images(launches):
    for launch in reversed(launches):
        if launch['links']['flickr']['original']:
            return launch['id']
    return None


def fetch_launch_images(launch_id):
    url_launch = f'https://api.spacexdata.com/v5/launches/{launch_id}'
    response = requests.get(url_launch)
    response.raise_for_status()
    launch_data = response.json()
    images_url = launch_data['links']['flickr']['original']
    images_dir = Path("spacex_images")
    images_dir.mkdir(parents=True, exist_ok=True)

    for index, images in enumerate(images_url, start=1):
        filename = f"spacex_{index}.jpg"
        file_path = images_dir / filename
        download_image(images, file_path)


def main():
    parser = argparse.ArgumentParser(
        description='Скачивание фото запусков SpaceX'
    )
    parser.add_argument(
        '--launch_id',
        type=str,
        help='ID конкретного запуска (если не указать, скачает последний с фото)'
    )
    args = parser.parse_args()
    if not args.launch_id:
        launches = get_all_launches()
        launch_id = get_last_launch_with_images(launches)
        if not launch_id:
            print("Нет запусков с фотографиями")
            return
    else:
        launch_id = args.launch_id
    fetch_launch_images(launch_id)


if __name__ == "__main__":
    main()
