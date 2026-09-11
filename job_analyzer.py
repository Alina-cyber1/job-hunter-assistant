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
        """
        Анализирует вакансию и возвращает решение.
        
        Возвращает словарь с полями:
        - should_apply: bool — стоит ли откликаться
        - match_score: float — процент совпадения (0-100)
        - reason: str — причина, если не подходит
        - matched_skills: list — навыки, которые совпали
        - missing_skills: list — навыки, которые не совпали
        """
        
        # 1. Проверка на удалённую работу (если фильтр уже не сработал)
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
        
        if not name_is_relevant:
            # Если название не содержит ключевых слов — всё равно проверяем описание
            # Но снижаем балл
            name_bonus = 0
        else:
            name_bonus = 10  # Бонус за релевантное название
        
        # 3. Объединяем требования и обязанности для анализа
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
            # Проверяем, есть ли навык в тексте вакансии
            # Используем границы слов для точного поиска
            pattern = r'\b' + re.escape(skill) + r'\b'
            if re.search(pattern, text):
                matched_skills.append(skill)
            else:
                missing_skills.append(skill)
        
        # 5. Вычисляем процент совпадения
        total_skills = len(self.my_skills)
        if total_skills == 0:
            match_score = 0
        else:
            match_score = (len(matched_skills) / total_skills) * 100
        
        # 6. Добавляем бонус за релевантное название
        match_score = min(match_score + name_bonus, 100)
        
        # 7. Проверка на минимальное количество совпадений
        # Нельзя откликаться, если совпало меньше 3 навыков
        if len(matched_skills) < 1:
            return {
                "should_apply": False,
                "match_score": round(match_score, 1),
                "reason": f"Совпало только {len(matched_skills)} навыков (минимум 3)",
                "matched_skills": matched_skills[:5],
                "missing_skills": missing_skills[:5]
            }
        
        # 8. Проверяем наличие хотя бы одного ключевого навыка
        key_skills = ["python", "ml", "ai", "machine learning", "data science", "rag", "llm"]
        has_key_skill = any(skill in matched_skills for skill in key_skills)
        
        if not has_key_skill:
            return {
                "should_apply": False,
                "match_score": round(match_score, 1),
                "reason": "Нет ключевых навыков (Python, ML, AI, RAG, LLM)",
                "matched_skills": matched_skills[:5],
                "missing_skills": missing_skills[:5]
            }
        
        # 9. Финальное решение
        should_apply = match_score >= 30  # Константа из config.py
        
        return {
            "should_apply": should_apply,
            "match_score": round(match_score, 1),
            "reason": "Подходит" if should_apply else f"Совпадение {match_score:.1f}% (ниже порога 70%)",
            "matched_skills": matched_skills[:10],  # Топ-10 совпавших
            "missing_skills": missing_skills[:5],   # Топ-5 недостающих
            "matched_count": len(matched_skills),
            "total_skills": total_skills
        }
