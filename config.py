import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

LOG_CHAT_ID = os.getenv("LOG_CHAT_ID")
if LOG_CHAT_ID:
    try:
        LOG_CHAT_ID = int(LOG_CHAT_ID)
    except ValueError:
        pass

if not all([BOT_TOKEN, GROQ_API_KEY]):
    logging.error("Missing required environment variables (BOT_TOKEN, GROQ_API_KEY).")
    sys.exit(1)
