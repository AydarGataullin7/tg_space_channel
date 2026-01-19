import telegram
import os
from dotenv import load_dotenv


def main():
    load_dotenv()
    tg_token = os.getenv("TG_TOKEN")

    bot = telegram.Bot(token=tg_token)
    updates = bot.get_updates()

    with open('nasa_images/nasa_5.jpg', 'rb') as photo_file:
        bot.send_photo(
            chat_id='@all_ab_sp',
            photo=photo_file
        )


if __name__ == "__main__":
    main()
