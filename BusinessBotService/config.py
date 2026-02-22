import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    API_ENDPOINT = os.getenv('API_ENDPOINT')
    
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN not found in .env file")

config = Config()
