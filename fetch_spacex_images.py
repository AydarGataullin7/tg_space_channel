import requests
from pathlib import Path
from urllib.parse import urlsplit, unquote
from helpers import download_image
import argparse


def fetch_spacex_last_launch(launch_ID=None):
    url = 'https://api.spacexdata.com/v5/launches'
    response = requests.get(url)
    launches = response.json()
    if launch_ID is None:
        for launch in reversed(launches):
            if launch['links']['flickr']['original']:
                launch_ID = launch['id']
                break
    url_launch = f'https://api.spacexdata.com/v5/launches/{launch_ID}'
    response = requests.get(url_launch)
    response.raise_for_status()
    data = response.json()
    images_url = data['links']['flickr']['original']
    images_dir = Path("spacex_images")
    images_dir.mkdir(parents=True, exist_ok=True)

    for index, images in enumerate(images_url, start=1):
        filename = (f"spacex_{index}.jpg")
        file_path = images_dir / filename
        download_image(images, file_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--launch_ID')
    args = parser.parse_args()
    fetch_spacex_last_launch(args.launch_ID)


if __name__ == "__main__":
    main()
