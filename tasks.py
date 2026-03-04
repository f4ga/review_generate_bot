import time
import random
import requests
from celery import Celery
from config import config

app = Celery("tasks", broker=config.REDIS_URL, backend=config.REDIS_URL)


def call_gigachat_api(product_name: str) -> str:
    """Генерация отзыва через GigaChat с повторными попытками при 429"""
    from gigachat import GigaChat
    from gigachat.exceptions import ResponseError

    max_retries = 3
    for attempt in range(max_retries):
        try:
            with GigaChat(
                credentials=config.GIGACHAT_AUTH_KEY,
                verify_ssl_certs=False,
                model=config.GIGACHAT_MODEL,
                scope=config.GIGACHAT_SCOPE,
                timeout=config.GIGACHAT_TIMEOUT,
            ) as giga:
                # Детальный промпт с акцентом на отсутствие форматирования
                prompt = (
                    f"Напиши развернутый отзыв на товар '{product_name}' от лица довольного покупателя. "
                    f"Отзыв должен быть естественным, подробным, без использования символов форматирования "
                    f"(звездочек, решеток, подчеркиваний). Не используй * # _ для выделения текста. "
                    f"Пиши обычным текстом, как реальный пользователь в интернет-магазине. "
                    f"Опиши достоинства, качество, впечатления. Отзыв должен быть позитивным и правдоподобным. "
                    f"Не используй markdown или HTML разметку. Только простой текст."
                )
                response = giga.chat(prompt)  # Передаём строку
                return response.choices[0].message.content
        except ResponseError as e:
            if e.status_code == 429 and attempt < max_retries - 1:
                wait = (2**attempt) + random.random()
                print(f"Rate limit (429), повтор через {wait:.2f} сек...")
                time.sleep(wait)
            else:
                return f"⚠️ Ошибка GigaChat: {str(e)}"
        except Exception as e:
            return f"⚠️ Ошибка при обращении к GigaChat: {str(e)}"
    return "⚠️ Не удалось получить ответ после нескольких попыток"


def send_telegram_message_sync(user_id: int, text: str):
    """Синхронная отправка сообщения через Telegram Bot API"""
    url = f"https://api.telegram.org/bot{config.BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": user_id,
        "text": text,
        "parse_mode": "HTML",  # можно отключить, если не нужно
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Не удалось отправить сообщение пользователю {user_id}: {e}")


@app.task
def generate_review(product_name: str, user_id: int):
    review = call_gigachat_api(product_name)
    send_telegram_message_sync(user_id, f"✅ Ваш отзыв готов:\n\n{review}")
    return review
