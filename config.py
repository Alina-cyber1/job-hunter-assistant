import os
from dotenv import load_dotenv

load_dotenv()

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# GigaChat
GIGACHAT_SECRET = os.getenv("GIGACHAT_SECRET")

# Параметры поиска
SEARCH_QUERY = "AI/ML разработчик"
AREA_ID = 0  # 0 = вся Россия
PER_PAGE = 20
MIN_MATCH_SCORE = 12

# Фильтр по типу занятости
SCHEDULE = "remote"  # только удалённая работа

# Дополнительные фильтры (опционально)
# EXPERIENCE = "between1And3"  # опыт от 1 до 3 лет
# EMPLOYMENT = "full"  # полная занятость
