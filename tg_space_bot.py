import telegram
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")
    chat_id = os.getenv("TG_CHAT_ID")
    bot = telegram.Bot(token=tg_token)
    bot.get_updates()
    with open('nasa_images/nasa_5.jpg', 'rb') as photo_file:
        bot.send_photo(
            chat_id=chat_id,
            photo=photo_file
        )


if __name__ == "__main__":
    main()
