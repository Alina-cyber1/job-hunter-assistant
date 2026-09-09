def send_vacancy_report(vacancy: dict, analysis: dict, cover_letter: str):
    """Формирует и отправляет отчёт по вакансии"""
    
    # Информация о графике
    schedule_info = "🌍 Удалённо" if vacancy.get("is_remote") else "🏢 В офисе"
    
    # Информация о зарплате
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

📌 <b>{vacancy.get('name')}</b>
🏢 {vacancy.get('company')}
💰 {salary_text}
{schedule_info}

📊 <b>Совпадение:</b> {analysis.get('match_score')}%
✅ <b>Совпавшие навыки:</b> {', '.join(analysis.get('matched_skills', [])[:5])}
❌ <b>Недостающие навыки:</b> {', '.join(analysis.get('missing_skills', [])[:3])}

🔗 <a href="{vacancy.get('url')}">Перейти к вакансии</a>

---
📝 <b>Готовое сопроводительное письмо:</b>
{cover_letter}

---
<i>Скопируйте письмо и отправьте через ссылку выше</i>
"""
    
    send_telegram_message(message)
