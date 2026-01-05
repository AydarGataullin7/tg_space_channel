import telegram
import os
from dotenv import load_dotenv

load_dotenv()
TG_TOKEN = os.getenv("TG_TOKEN")
bot = telegram.Bot(token=TG_TOKEN)
updates = bot.get_updates()
bot.send_message(
    chat_id='@all_ab_sp', text="Text for test😉")
