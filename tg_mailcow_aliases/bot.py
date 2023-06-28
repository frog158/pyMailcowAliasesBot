import os
import telebot
import logging

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN", "error")
USER_ID = os.getenv("USER_ID", "error")
