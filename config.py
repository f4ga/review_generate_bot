import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    if not BOT_TOKEN:
        raise ValueError("❌ BOT_TOKEN не найден!")

    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

    # GigaChat
    GIGACHAT_AUTH_KEY = os.getenv("GIGACHAT_AUTH_KEY")
    if not GIGACHAT_AUTH_KEY:
        raise ValueError("❌ GIGACHAT_AUTH_KEY не найден!")

    GIGACHAT_MODEL = os.getenv("GIGACHAT_MODEL", "GigaChat")
    GIGACHAT_SCOPE = os.getenv("GIGACHAT_SCOPE", "GIGACHAT_API_PERS")
    GIGACHAT_TIMEOUT = int(os.getenv("GIGACHAT_TIMEOUT", 60))


config = Config()
