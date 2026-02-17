import os

from dotenv import load_dotenv

def get_db_url() -> str:
    load_dotenv()
    return os.getenv("DB_URL")

