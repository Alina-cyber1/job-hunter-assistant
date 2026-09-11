from hh_parser import fetch_vacancies
from job_analyzer import JobAnalyzer
from cover_letter_generator import generate_cover_letter
from telegram_sender import send_vacancy_report
from config import MIN_MATCH_SCORE

def main():
    print("Запуск Job Hunter Assistant...")
    
    # 1. Получаем вакансии
    vacancies = fetch_vacancies()
    print(f" Найдено вакансий: {len(vacancies)}")
    
    # 2. Анализируем каждую
    analyzer = JobAnalyzer()
    found_count = 0
    
    for vacancy in vacancies:
        analysis = analyzer.analyze(vacancy)
        
        if analysis.get("should_apply"):
            found_count += 1
            print(f"Подходит: {vacancy.get('name')} ({analysis.get('match_score')}%)")
            
            # 3. Генерируем письмо
            cover_letter = generate_cover_letter(vacancy, analysis.get("matched_skills", []))
            
            # 4. Отправляем в Telegram
            send_vacancy_report(vacancy, analysis, cover_letter)
        else:
            print(f" Не подходит: {vacancy.get('name')} ({analysis.get('match_score')}%)")
    
    print(f"\n Найдено подходящих вакансий: {found_count}")

if __name__ == "__main__":
    main()
