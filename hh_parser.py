# hh_parser.py
import requests
import xml.etree.ElementTree as ET

def fetch_vacancies():
    url = "https://career.habr.com/vacancies/rss"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (compatible; JobHunter/1.0)",
        "Accept": "application/rss+xml, application/xml"
    }
    
    params = {
        "q": "AI ML Python",
        "type": "all",
        "remote": "true",
        "s": "100"
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=30)
        
        if response.status_code != 200:
            print(f"Habr Career вернул код: {response.status_code}")
            return []
        
        root = ET.fromstring(response.content)
        vacancies = []
        
        for item in root.findall(".//item"):
            title = item.findtext("title", "").strip()
            link = item.findtext("link", "").strip()
            description = item.findtext("description", "").strip()
            pub_date = item.findtext("pubDate", "").strip()
            
            if not title or not link:
                continue
            
            vacancy_id = link.rstrip("/").split("/")[-1] if link else ""
            
            vacancies.append({
                "id": vacancy_id,
                "name": title,
                "company": "Habr Career",
                "url": link,
                "requirement": description,
                "responsibility": description,
                "salary_from": 0,
                "salary_to": 0,
                "salary_currency": "RUR",
                "is_remote": True,
                "schedule_name": "Удалённо",
                "published": pub_date
            })
        
        print(f"Habr Career: найдено {len(vacancies)} вакансий")
        return vacancies
    
    except Exception as e:
        print(f"Ошибка запроса Habr Career: {e}")
        return []
