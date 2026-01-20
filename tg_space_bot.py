import telegram
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    photo_path = os.getenv("TG_PHOTO_PATH", "nasa_images/nasa_5.jpg")

    bot = telegram.Bot(token=tg_token)
    bot.get_updates()

    with open(photo_path, 'rb') as photo_file:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo_file
        )


if __name__ == "__main__":
    main()
