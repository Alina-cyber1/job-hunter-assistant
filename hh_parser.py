# hh_parser.py
import requests
import xml.etree.ElementTree as ET

def fetch_vacancies():
    """
    Ищет вакансии через RSS-ленту Habr Career.
    Параметры не передаём — фильтруем сами.
    """
    url = "https://career.habr.com/vacancies/rss"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; JobHunter/1.0)"
    }
    
    # Ключевые слова для фильтрации
    keywords = [
        "python", "ml", "ai", "machine learning", "data science",
        "data scientist", "аналитик данных", "llm", "nlp", "rag",
        "pytorch", "tensorflow", "pandas", "numpy", "sql"
    ]
    
    try:
        response = requests.get(url, headers=headers, timeout=30)
        print(f"Статус ответа Habr Career: {response.status_code}")
        
        if response.status_code != 200:
            print(f"Habr Career вернул код: {response.status_code}")
            return []
        
        root = ET.fromstring(response.content)
        vacancies = []
        total_found = 0
        
        for item in root.findall(".//item"):
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            description = item.findtext("description", "").strip()
            author = item.findtext("author", "").strip()
            pub_date = item.findtext("pubDate", "").strip()
            
            if not title or not link:
                continue
            
            total_found += 1
            
            # Фильтруем: ищем ключевые слова в названии + описании
            text_to_check = (title + " " + description).lower()
            matches = [kw for kw in keywords if kw in text_to_check]
            
            if not matches:
                continue  # не наша вакансия — пропускаем
            
            vacancy_id = link.rstrip("/").split("/")[-1] if link else ""
            
            vacancies.append({
                "id": vacancy_id,
                "name": title,
                "company": author or "Habr Career",
                "url": link,
                "requirement": description,
                "responsibility": description,
                "salary_from": 0,
                "salary_to": 0,
                "salary_currency": "RUR",
                "is_remote": True,
                "schedule_name": "Удалённо",
                "published": pub_date,
                "matched_keywords": matches
            })
        
        print(f"Habr Career: всего {total_found} вакансий, из них подходящих: {len(vacancies)}")
        return vacancies
    
    except Exception as e:
        print(f"Ошибка запроса Habr Career: {e}")
        return []
