import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv('BOT_TOKEN')
    if not BOT_TOKEN:
        raise ValueError('Токен бота не найден в .env файле')
    DATABASE_URL = os.getenv('DATABASE_URL')


config = Config()
