import argparse
import os
import random
import time
import telegram
from dotenv import load_dotenv


def get_image_files(image_folder):
    image_files = []
    for folder in os.listdir(image_folder):
        folder_path = os.path.join(image_folder, folder)
        if os.path.isdir(folder_path):
            for filename in os.listdir(folder_path):
                if filename.lower().endswith(('.jpg', '.png', '.jpeg')):
                    image_files.append(os.path.join(folder_path, filename))
    return image_files


def main():
    load_dotenv()
    env_delay = os.getenv('PUBLISH_DELAY_HOURS', '4')
    default_delay = int(env_delay)
    chat_id = os.getenv('TG_CHAT_ID')
    parser = argparse.ArgumentParser(
        description='Автоматическая публикация фото в Telegram-канал'
    )
    parser.add_argument(
        '--delay',
        type=int,
        default=default_delay,
        help='Задержка между публикациями в часах (по умолчанию: 4)',
        choices=range(1, 25)
    )
    args = parser.parse_args()

    second_in_hour = 3600
    delay_seconds = args.delay * second_in_hour

    TG_TOKEN = os.getenv('TG_TOKEN')

    bot = telegram.Bot(token=TG_TOKEN)
    image_folder = "."

    while True:
        image_files = get_image_files(image_folder)

        if not image_files:
            print("Нет фотографий для публикации.")
            time.sleep(delay_seconds)
            continue

        random.shuffle(image_files)

        for image_path in image_files:
            try:
                with open(image_path, 'rb') as photo:
                    bot.send_photo(chat_id=chat_id, photo=photo)
                    time.sleep(delay_seconds)
            except (telegram.error.TelegramError, FileNotFoundError) as e:
                print(f"Ошибка при публикации {image_path}: {e}")


if __name__ == "__main__":
    main()
