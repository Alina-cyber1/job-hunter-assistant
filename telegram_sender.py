# telegram_sender.py
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_message(text: str) -> bool:
    """Отправляет сообщение в Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не заданы")
        return False
    
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    
    try:
        response = requests.post(url, data=data, timeout=30)
        if response.status_code == 200:
            return True
        else:
            print(f"Telegram вернул код: {response.status_code}")
            print(f"Ответ: {response.text[:300]}")
            return False
    except Exception as e:
        print(f"Ошибка отправки в Telegram: {e}")
        return False


def send_startup_message():
    """Отправляет приветствие при запуске бота (для проверки связи)"""
    message = """🤖 <b>Job Hunter Assistant запущен!</b>

Что умеет:
🔍 Ищет вакансии на Habr Career
📊 Анализирует по вашему резюме
📝 Генерирует сопроводительные письма
📩 Отправляет результаты сюда

<b>Что дальше:</b>
Подождите 1-2 минуты — сейчас придёт отчёт по найденным вакансиям.

⚠️ Если сообщения не приходят — проверьте ID у @userinfobot."""
    
    return send_telegram_message(message)


def send_vacancy_report(vacancy: dict, analysis: dict, cover_letter: str):
    """Отправляет отчёт по вакансии"""
    schedule_info = "Удалённо" if vacancy.get("is_remote") else "В офисе"
    
    message = f"""
🔍 <b>Найдена подходящая вакансия!</b>

📌 <b>{vacancy.get('name')}</b>
🏢 {vacancy.get('company')}
{schedule_info}

📊 <b>Совпадение:</b> {analysis.get('match_score')}%
✅ <b>Совпавшие навыки:</b> {', '.join(analysis.get('matched_skills', [])[:5])}

🔗 <a href="{vacancy.get('url')}">Перейти к вакансии</a>

---
📝 <b>Готовое сопроводительное письмо:</b>
{cover_letter}
"""
    
    result = send_telegram_message(message)
    if result:
        print(f"Отчёт отправлен: {vacancy.get('name')}")
    else:
        print(f"Не удалось отправить: {vacancy.get('name')}")
