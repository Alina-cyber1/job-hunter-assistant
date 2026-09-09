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
AREA_ID = 0  # 0 = вся Россия (все регионы)
PER_PAGE = 20
MIN_MATCH_SCORE = 70

# Фильтр по типу занятости
SCHEDULE = "remote"  # только удалённая работа
# Другие варианты:
# "fullDay" — полный день
# "part" — частичная занятость
# "project" — проектная работа
# "volunteer" — волонтёрство
# "internship" — стажировка
