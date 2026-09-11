import requests
from config import SEARCH_QUERY, AREA_ID, PER_PAGE, SCHEDULE

def fetch_vacancies():
    """Получает список вакансий с hh.ru с фильтром по удалённой работе"""
    url = "https://api.hh.ru/vacancies"
    
    # ВАЖНО: заголовки, чтобы hh.ru не блокировал запрос
    headers = {
        "User-Agent": "JobHunterAssistant/1.0 (alina_has@mail.ru)",
        "Accept": "application/json"
    }
    
    params = {
        "text": SEARCH_QUERY,
        "area": AREA_ID,
        "per_page": PER_PAGE,
        "schedule": SCHEDULE,
        "only_with_salary": True
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"Ошибка API: {response.status_code}")
            print(f"Ответ сервера: {response.text[:500]}")
            return []
        
        items = response.json().get("items", [])
        vacancies = []
        
        for item in items:
            schedule = item.get("schedule", {})
            is_remote = schedule.get("id") == "remote" if schedule else False
            
            if not is_remote:
                continue
            
            vacancies.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "company": item.get("employer", {}).get("name", "Не указана"),
                "url": item.get("alternate_url"),
                "requirement": item.get("snippet", {}).get("requirement", ""),
                "responsibility": item.get("snippet", {}).get("responsibility", ""),
                "salary_from": item.get("salary", {}).get("from", 0) if item.get("salary") else 0,
                "salary_to": item.get("salary", {}).get("to", 0) if item.get("salary") else 0,
                "salary_currency": item.get("salary", {}).get("currency", "RUR") if item.get("salary") else "RUR",
                "is_remote": is_remote,
                "schedule_name": schedule.get("name", "Не указан") if schedule else "Не указан"
            })
        
        return vacancies
    
    except Exception as e:
        print(f"Ошибка запроса: {e}")
        return []
