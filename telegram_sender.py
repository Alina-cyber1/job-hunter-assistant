# telegram_sender.py
import requests
import os
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID


def send_telegram_message(text: str) -> bool:
    """Отправляет сообщение в Telegram"""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print(" TELEGRAM_BOT_TOKEN или TELEGRAM_CHAT_ID не заданы")
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
            print(f" Telegram вернул код: {response.status_code}")
            print(f"Ответ: {response.text[:300]}")
            return False
    except Exception as e:
        print(f" Ошибка отправки в Telegram: {e}")
        return False


def send_vacancy_report(vacancy: dict, analysis: dict, cover_letter: str):
    """Формирует и отправляет отчёт по вакансии"""
    
    schedule_info = " Удалённо" if vacancy.get("is_remote") else " В офисе"
    
    salary_text = "Зарплата не указана"
    if vacancy.get("salary_from") or vacancy.get("salary_to"):
        parts = []
        if vacancy.get("salary_from"):
            parts.append(f"от {vacancy.get('salary_from'):,}")
        if vacancy.get("salary_to"):
            parts.append(f"до {vacancy.get('salary_to'):,}")
        salary_text = f"{' '.join(parts)} {vacancy.get('salary_currency', 'RUR')}"
    
    message = f"""
🔍 <b>Найдена подходящая вакансия!</b>

 <b>{vacancy.get('name')}</b>
 {vacancy.get('company')}
 {salary_text}
{schedule_info}

 <b>Совпадение:</b> {analysis.get('match_score')}%
 <b>Совпавшие навыки:</b> {', '.join(analysis.get('matched_skills', [])[:5])}

 <a href="{vacancy.get('url')}">Перейти к вакансии</a>

---
 <b>Готовое сопроводительное письмо:</b>
{cover_letter}

---
<i>Скопируйте письмо и отправьте через ссылку выше</i>
"""
    
    result = send_telegram_message(message)
    if result:
        print(f" Отчёт отправлен в Telegram: {vacancy.get('name')}")
    else:
        print(f" Не удалось отправить: {vacancy.get('name')}")
