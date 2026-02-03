"""
Gemini API integration for searching and analyzing articles
"""
import google.generativeai as genai
from typing import List, Dict
import json
import config
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class GeminiSearchEngine:
    def __init__(self):
        if not config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY not set in configuration")
        
        genai.configure(api_key=config.GEMINI_API_KEY)
        self.model = genai.GenerativeModel('gemini-pro')
    
    def search_articles(self, keyword: str, num_results: int = 10) -> List[Dict]:
        """
        Search for articles using Gemini API
        Note: Gemini doesn't have direct web search, so we ask it to generate
        search queries and provide guidance on finding relevant content
        """
        prompt = f"""
        Я ищу статьи и новости по теме: "{keyword}"
        
        Контекст: Компания занимается энергоаудитом, тепловизионным обследованием зданий,
        испытанием вентиляционных систем, проверкой герметичности помещений.
        
        Предложи {num_results} релевантных источников информации или тем для статей, которые могли бы
        быть интересны для новостного блога компании energo-audit.by.
        
        Для каждого предложения укажи:
        1. Заголовок статьи
        2. Краткое описание (2-3 предложения)
        3. Почему это релевантно для аудитории
        4. Предполагаемый источник или тип контента
        
        Верни ответ в формате JSON:
        {{
            "articles": [
                {{
                    "title": "...",
                    "description": "...",
                    "relevance": "...",
                    "source_type": "..."
                }}
            ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            # Extract JSON from response
            text = response.text
            
            # Try to find JSON in the response
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                result = json.loads(json_str)
                return result.get('articles', [])
            else:
                logger.warning(f"No JSON found in response for keyword: {keyword}")
                return []
                
        except Exception as e:
            logger.error(f"Error searching with Gemini: {e}")
            return []
    
    def analyze_article(self, article: Dict) -> Dict:
        """
        Analyze an article using Gemini to determine its quality and relevance
        Returns scores and analysis
        """
        prompt = f"""
        Проанализируй следующую статью для новостного блога компании по энергоаудиту:
        
        Заголовок: {article.get('title', '')}
        Описание: {article.get('description', '')}
        Контент: {article.get('content', '')[:1000]}
        
        Оцени статью по следующим критериям (от 1 до 10):
        1. Релевантность для аудитории (энергоаудит, тепловизия, вентиляция)
        2. Качество контента и информативность
        3. Актуальность информации
        4. Потенциал для привлечения клиентов
        5. Уникальность и ценность информации
        
        Также определи:
        - Ключевые темы статьи
        - Целевая аудитория
        - Рекомендации по адаптации для блога
        - Предложения для заголовка в соц.сетях
        
        Верни ответ в формате JSON:
        {{
            "scores": {{
                "relevance": 0-10,
                "quality": 0-10,
                "timeliness": 0-10,
                "business_value": 0-10,
                "uniqueness": 0-10,
                "overall": 0-10
            }},
            "key_topics": ["тема1", "тема2"],
            "target_audience": "...",
            "adaptation_tips": "...",
            "social_media_title": "..."
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            # Extract JSON from response
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                analysis = json.loads(json_str)
                return analysis
            else:
                logger.warning("No JSON found in analysis response")
                return self._default_analysis()
                
        except Exception as e:
            logger.error(f"Error analyzing article: {e}")
            return self._default_analysis()
    
    def _default_analysis(self) -> Dict:
        """Return default analysis structure"""
        return {
            "scores": {
                "relevance": 5.0,
                "quality": 5.0,
                "timeliness": 5.0,
                "business_value": 5.0,
                "uniqueness": 5.0,
                "overall": 5.0
            },
            "key_topics": [],
            "target_audience": "общая аудитория",
            "adaptation_tips": "требуется ручная проверка",
            "social_media_title": ""
        }
    
    def generate_blog_post(self, article: Dict) -> Dict:
        """
        Generate a blog post based on the article using Gemini
        """
        prompt = f"""
        На основе следующей информации создай статью для блога компании по энергоаудиту:
        
        Исходный заголовок: {article.get('title', '')}
        Исходный контент: {article.get('description', '')}
        
        Создай:
        1. Привлекательный заголовок (SEO-оптимизированный)
        2. Вступление (2-3 абзаца)
        3. Основной текст (разбитый на разделы с подзаголовками)
        4. Заключение с призывом к действию
        5. Мета-описание для SEO (до 160 символов)
        6. Теги для WordPress
        
        Учитывай услуги компании: {', '.join(config.SERVICES.values())}
        
        Верни в формате JSON:
        {{
            "title": "...",
            "intro": "...",
            "body": "...",
            "conclusion": "...",
            "meta_description": "...",
            "tags": ["тег1", "тег2"]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            text = response.text
            
            start_idx = text.find('{')
            end_idx = text.rfind('}') + 1
            
            if start_idx != -1 and end_idx > start_idx:
                json_str = text[start_idx:end_idx]
                blog_post = json.loads(json_str)
                return blog_post
            else:
                logger.warning("No JSON found in blog post generation")
                return self._default_blog_post(article)
                
        except Exception as e:
            logger.error(f"Error generating blog post: {e}")
            return self._default_blog_post(article)
    
    def _default_blog_post(self, article: Dict) -> Dict:
        """Return default blog post structure"""
        return {
            "title": article.get('title', 'Новая статья'),
            "intro": article.get('description', ''),
            "body": article.get('content', ''),
            "conclusion": "Свяжитесь с нами для получения профессиональной консультации.",
            "meta_description": article.get('description', '')[:160],
            "tags": []
        }
