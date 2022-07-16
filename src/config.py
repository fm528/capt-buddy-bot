import os
from dotenv import load_dotenv

load_dotenv()

ANGEL_BOT_TOKEN = os.environ['BOT_TOKEN']
PLAYERS_FILENAME = os.environ['PLAYERS_FILENAME']
CHAT_ID_JSON = os.environ['CHAT_ID_JSON']
