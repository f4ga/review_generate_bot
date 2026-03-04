# 🤖 Генератор отзывов на базе AI (Celery + GigaChat)

[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://python.org)
[![Aiogram](https://img.shields.io/badge/aiogram-3.26.0-green.svg)](https://docs.aiogram.dev)
[![Celery](https://img.shields.io/badge/celery-5.6.2-brightgreen.svg)](https://docs.celeryq.dev)
[![Redis](https://img.shields.io/badge/redis-6.4.0-red.svg)](https://redis.io)
[![GigaChat](https://img.shields.io/badge/GigaChat-Sber-ff69b4.svg)](https://developers.sber.ru/gigachat)
[![Flower](https://img.shields.io/badge/flower-2.0.1-yellow.svg)](https://flower.readthedocs.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Telegram‑бот, который генерирует правдоподобные отзывы на товары с помощью нейросети GigaChat. Запросы обрабатываются асинхронно в очереди Celery — пользователь не ждёт ответа, а получает уведомление, когда отзыв готов.**

---

## ✨ Возможности

- 🧠 **Интеграция с GigaChat** (Сбер) — российская LLM, отличное качество русского языка.
- ⚡ **Асинхронная обработка** — Celery + Redis: пользователь сразу получает подтверждение, а генерация происходит в фоне.
- 📦 **Мониторинг задач** — Flower веб‑интерфейс для отслеживания очереди.
- 🐳 **Docker поддержка** — полная контейнеризация (бот, воркер, Redis, Flower) через `docker-compose`.
- 🔁 **Автоматические повторные попытки** при превышении лимитов API (429).
- 🚫 **Чистый текст** — промпт настроен так, чтобы в ответах не было звёздочек, решёток и прочего форматирования.
- 📱 **Простота использования** — отправь название товара и получи готовый отзыв через несколько секунд.

---

## 🛠 Технологический стек

| Компонент       | Технология                                                             |
|-----------------|------------------------------------------------------------------------|
| Язык            | Python 3.11+                                                           |
| Telegram API    | [aiogram](https://docs.aiogram.dev) 3.26.0                             |
| Очередь задач   | [Celery](https://docs.celeryq.dev) 5.6.2 + [Redis](https://redis.io)  |
| Мониторинг      | [Flower](https://flower.readthedocs.io) 2.0.1                          |
| LLM API         | [GigaChat](https://developers.sber.ru/gigachat) (Сбер)                 |
| Контейнеризация | Docker, Docker Compose                                                  |

---

## 🚀 Быстрый старт

### 🔧 Предварительные требования

- Установленные [Docker](https://docs.docker.com/get-docker/) и [Docker Compose](https://docs.docker.com/compose/install/) (для контейнерного запуска)  
  **ИЛИ** Python 3.11+, Redis, pip
- Аккаунт в [Sber Developers](https://developers.sber.ru/) и **Authorization Key** для GigaChat
- Токен Telegram‑бота (получить у [@BotFather](https://t.me/botfather))

### 📦 Установка

#### 1. Клонирование репозитория
```bash
git clone https://github.com/f4ga/review_generate_bot.git
cd review_generate_bot

2. Настройка переменных окружения

Скопируйте пример файла .env и заполните свои данные:
bash

cp .env.example .env

Отредактируйте .env:
env
```
# Telegram
BOT_TOKEN=ваш_токен_бота

# Redis
REDIS_URL=redis://localhost:6379/0

# GigaChat
GIGACHAT_AUTH_KEY=ваш_ключ_авторизации_гигачат
GIGACHAT_MODEL=GigaChat
GIGACHAT_SCOPE=GIGACHAT_API_PERS
GIGACHAT_TIMEOUT=60

    💡 Где взять ключ GigaChat?
    Зарегистрируйтесь на developers.sber.ru, создайте проект GigaChat и скопируйте Authorization Key (показывается только один раз!).

🐳 Запуск через Docker Compose (рекомендуется)
bash

docker-compose up -d

Будут запущены четыре контейнера:

    redis — брокер сообщений

    tg_bot — сам бот

    celery_worker — воркер, обрабатывающий задачи

    flower — веб‑мониторинг на порту 5555

Проверьте логи:
bash

docker-compose logs -f

Теперь бот уже работает! Напишите ему в Telegram команду /start.
🖥 Локальный запуск (без Docker)
1. Установка зависимостей

Рекомендуется использовать виртуальное окружение:
bash

python -m venv venv
source venv/bin/activate      # Linux/macOS
venv\Scripts\activate         # Windows

Установка пакетов:
bash

pip install -r requirements.txt

### 2. Запуск Redis

Убедитесь, что Redis запущен локально. Если нет:
bash

# через systemd (Linux)
sudo systemctl start redis

# или через Docker
docker run -d -p 6379:6379 redis

3. Запуск Celery worker

В отдельном терминале выполните:
bash

celery -A tasks worker --loglevel=info

4. Запуск бота

В другом терминале:
bash

python bot.py

5. Мониторинг Flower (опционально)
bash

celery -A tasks flower --port=5555

Откройте http://localhost:5555 для просмотра очереди задач.
📱 Использование бота

    Отправьте боту команду /start — он поприветствует вас.

    Просто напишите название товара (например, «крем для рук» или «набор отверток»).

    Бот мгновенно ответит: «⏳ Отзыв генерируется, подождите немного...»

    Через несколько секунд (обычно 3–7) придет готовый развернутый отзыв.

Пример ответа (без форматирования):
text

Отличная шариковая ручка! Пользуюсь уже неделю, пишет очень мягко, чернила не пачкают. Корпус приятный на ощупь, не скользит. Рекомендую к покупке!

📁 Структура проекта
text

.
├── .env.example           # Шаблон переменных окружения
├── .gitignore
├── Dockerfile             # Сборка образа для всех сервисов
├── docker-compose.yml     # Оркестрация контейнеров
├── requirements.txt       # Зависимости Python
├── README.md              # Этот файл
├── bot.py                 # Основной код Telegram‑бота
├── bot_instance.py        # Экземпляр бота (для импорта в задачи)
├── config.py              # Загрузка конфигурации из .env
└── tasks.py               # Celery задачи (генерация отзывов через GigaChat)

⚙️ Переменные окружения
Переменная	Описание	Обязательно	По умолчанию
BOT_TOKEN	Токен Telegram‑бота	✅	—
REDIS_URL	Адрес Redis‑сервера	❌	redis://localhost:6379/0
GIGACHAT_AUTH_KEY	Ключ авторизации GigaChat	✅	—
GIGACHAT_MODEL	Модель GigaChat	❌	GigaChat
GIGACHAT_SCOPE	Область доступа (PERS для физлиц)	❌	GIGACHAT_API_PERS
GIGACHAT_TIMEOUT	Таймаут запроса к API (сек)	❌	60
🧠 Как это работает

    Пользователь отправляет название товара боту.

    Хэндлер в bot.py ставит задачу в Celery (generate_review.delay(...)) и сразу отвечает «Отзыв генерируется…».

    Celery worker (процесс из tasks.py) забирает задачу и вызывает GigaChat API с детальным промптом.

    В случае ошибки 429 (Too Many Requests) задача автоматически повторяется с экспоненциальной задержкой.

    Полученный отзыв отправляется пользователю через прямой HTTP‑запрос к Telegram API (синхронно, без asyncio, чтобы избежать конфликтов циклов событий).

🤝 Участие в разработке

Будем рады вашим идеям и улучшениям!

    Форкните репозиторий.

    Создайте ветку для фичи (git checkout -b feature/amazing-feature).

    Закоммитьте изменения (git commit -m 'Add some amazing feature').

    Запушьте ветку (git push origin feature/amazing-feature).

    Откройте Pull Request.

📬 Контакты

Автор: f4ga
Проект: GitHub

Если возникли вопросы или предложения — создавайте Issue или пишите в Telegram: @ebssy
<p align="center"> Сделано с ❤️ и ☕️ в 2026 году </p> ```
