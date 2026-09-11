from hh_parser import fetch_vacancies
from job_analyzer import JobAnalyzer
from cover_letter_generator import generate_cover_letter
from telegram_sender import send_vacancy_report, send_telegram_message
from config import MIN_MATCH_SCORE


def main():
    print("Запуск Job Hunter Assistant...")
    
    vacancies = fetch_vacancies()
    print(f"Найдено вакансий: {len(vacancies)}")
    
    if not vacancies:
        send_telegram_message("⚠️ Habr Career не вернул вакансий. Возможно, RSS не работает.")
        return
    
    analyzer = JobAnalyzer()
    found_count = 0
    rejected_count = 0
    
    all_vacancies_text = "📋 <b>Найдено вакансий:</b>\n\n"
    
    for vacancy in vacancies:
        analysis = analyzer.analyze(vacancy)
        
        all_vacancies_text += f"• {vacancy.get('name')[:60]} — {analysis.get('match_score')}%\n"
        
        if analysis.get("should_apply"):
            found_count += 1
            cover_letter = generate_cover_letter(vacancy, analysis.get("matched_skills", []))
            send_vacancy_report(vacancy, analysis, cover_letter)
        else:
            rejected_count += 1
    
    print(f"\nНайдено подходящих: {found_count}")
    print(f"Отклонено: {rejected_count}")
    
    if found_count == 0:
        send_telegram_message(
            f"📊 <b>Job Hunter отчёт</b>\n\n"
            f"Найдено вакансий: {len(vacancies)}\n"
            f"Подходящих: {found_count}\n"
            f"Отклонено: {rejected_count}\n\n"
            f"<b>Все вакансии:</b>\n{all_vacancies_text[:2000]}"
        )


if __name__ == "__main__":
    main()
