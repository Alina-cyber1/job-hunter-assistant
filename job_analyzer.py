import re
from resume_parser import RESUME_TEXT

class JobAnalyzer:
    def __init__(self):
        self.resume_text = RESUME_TEXT.lower()
        
        # Ключевые навыки из вашего резюме (расширенный список)
        self.my_skills = [
            # Языки и технологии
            "python", "pandas", "numpy", "duckdb", "streamlit", "plotly",
            "scikit-learn", "sklearn", "tensorflow", "keras", "pytorch",
            
            # LLM и RAG
            "gigachat", "rag", "faiss", "langchain", "prompt engineering",
            
            # Базы данных и инфраструктура
            "sql", "postgresql", "mysql", "git", "docker", "linux", "bash",
            "airflow", "mlflow", "spark", "pyspark",
            
            # API и бэкенд
            "fastapi", "rest api", "api", "telegram bot",
            
            # Общие навыки
            "ml", "ai", "machine learning", "data science", "аналитика",
            "автоматизация", "дашборды", "визуализация", "hr analytics",
            "прогнозирование", "моделирование", "временные ряды",
            "обработка данных", "etl", "оптимизация"
        ]
        
        # Ключевые слова, которые могут встретиться в названии вакансии
        self.target_keywords = [
            "ai", "ml", "machine learning", "data science", "nlp", "llm", "rag",
            "аналитик", "data scientist", "разработчик", "python"
        ]
    
    def analyze(self, vacancy: dict) -> dict:
        # 1. Проверка на удалённую работу
        if not vacancy.get("is_remote", False):
            return {
                "should_apply": False,
                "match_score": 0,
                "reason": "Не удалённая работа",
                "matched_skills": [],
                "missing_skills": []
            }
        
        # 2. Проверка на релевантность по названию
        name = vacancy.get("name", "").lower()
        name_is_relevant = any(kw in name for kw in self.target_keywords)
        name_bonus = 10 if name_is_relevant else 0
        
        # 3. Объединяем требования и обязанности
        text = (
            vacancy.get("requirement", "") + " " + 
            vacancy.get("responsibility", "")
        ).lower()
        
        if not text:
            return {
                "should_apply": False,
                "match_score": 0,
                "reason": "Нет описания вакансии",
                "matched_skills": [],
                "missing_skills": []
            }
        
        # 4. Считаем совпадения навыков
        matched_skills = []
        missing_skills = []
        
        for skill in self.my_skills:
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        
        # 5. Вычисляем процент совпадения
        total_skills = len(self.my_skills)
        match_score = (len(matched_skills) / total_skills) * 100 if total_skills else 0
        
        # 6. Добавляем бонус за релевантное название
        match_score = min(match_score + name_bonus, 100)
        
        # === ОТЛАДКА ===
        print(f"  Вакансия: {vacancy.get('name')[:60]}")
        print(f"  Совпало навыков: {len(matched_skills)}")
        print(f"  Match score: {match_score:.1f}%")
        print(f"  Совпавшие: {matched_skills[:5]}")
        print("---")
        # === КОНЕЦ ОТЛАДКИ ===
        
        # 7. Проверка на минимум навыков
        if len(matched_skills) < 1:
            return {
                "should_apply": False,
                "match_score": round(match_score, 1),
                "reason": f"Совпало только {len(matched_skills)} навыков",
                "matched_skills": matched_skills[:5],
                "missing_skills": missing_skills[:5]
            }
        
        # 8. Проверяем наличие ключевого навыка
        key_skills = ["python", "ml", "ai", "machine learning", "data science", "rag", "llm"]
        has_key_skill = any(skill in matched_skills for skill in key_skills)
        
        if not has_key_skill:
            return {
                "should_apply": False,
                "match_score": round(match_score, 1),
                "reason": "Нет ключевых навыков",
                "matched_skills": matched_skills[:5],
                "missing_skills": missing_skills[:5]
            }
        
        # 9. Финальное решение
        should_apply = match_score >= 30
        
        return {
            "should_apply": should_apply,
            "match_score": round(match_score, 1),
            "reason": "Подходит" if should_apply else f"Совпадение {match_score:.1f}% (ниже порога)",
            "matched_skills": matched_skills[:10],
            "missing_skills": missing_skills[:5],
            "matched_count": len(matched_skills),
            "total_skills": total_skills
        }
