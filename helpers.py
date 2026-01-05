import requests
import os


def download_image(url, file_path):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    with open(file_path, "wb") as f:
        f.write(response.content)


def get_file_extension(url):
    url_file = urlsplit(url)
    path_of_url = url_file.path
    decoded_path = unquote(path_of_url)
    file_name = os.path.split(decoded_path)[1]
    extension = os.path.splitext(file_name)[1]
    return extension
