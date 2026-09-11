# cover_letter_generator.py
import os
from resume_parser import RESUME_TEXT

def generate_cover_letter(vacancy: dict, matched_skills: list) -> str:
    """Генерирует сопроводительное письмо"""
    try:
        from gigachat import GigaChat
        client = GigaChat(
            credentials=os.getenv("GIGACHAT_SECRET"),
            scope="GIGACHAT_API_PERS",
            verify_ssl_certs=False
        )
        
        prompt = f"""
        Напиши короткое сопроводительное письмо на русском для вакансии:

        Вакансия: {vacancy.get('name')}
        Компания: {vacancy.get('company')}
        Требования: {vacancy.get('requirement', 'Не указаны')}

        Мои ключевые навыки: {', '.join(matched_skills[:5])}

        Мой опыт (кратко):
        {RESUME_TEXT[:1000]}

        Требования: 3-4 предложения, деловой стиль, подчеркнуть соответствие.
        Только текст письма.
        """
        
        response = client.chat(prompt)
        return response.choices[0].message.content.strip()
    
    except Exception as e:
        return f"""Здравствуйте!

Меня заинтересовала вакансия {vacancy.get('name')} в компании {vacancy.get('company')}.
Мой опыт в разработке на Python и создании AI/ML-решений полностью соответствует требованиям.

Буду рада обсудить детали на собеседовании.

С уважением, Алина"""
