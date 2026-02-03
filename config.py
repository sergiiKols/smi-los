"""
Configuration module for the content search and publishing system
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Gemini API Configuration
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')

# WordPress Configuration
WORDPRESS_URL = os.getenv('WORDPRESS_URL', 'https://energo-audit.by')
WORDPRESS_USERNAME = os.getenv('WORDPRESS_USERNAME', '')
WORDPRESS_PASSWORD = os.getenv('WORDPRESS_PASSWORD', '')

# Facebook Configuration
FACEBOOK_ACCESS_TOKEN = os.getenv('FACEBOOK_ACCESS_TOKEN', '')
FACEBOOK_PAGE_ID = os.getenv('FACEBOOK_PAGE_ID', '')

# Instagram Configuration
INSTAGRAM_ACCESS_TOKEN = os.getenv('INSTAGRAM_ACCESS_TOKEN', '')
INSTAGRAM_BUSINESS_ACCOUNT_ID = os.getenv('INSTAGRAM_BUSINESS_ACCOUNT_ID', '')

# Scheduling Configuration
SEARCH_HOUR = int(os.getenv('SEARCH_HOUR', 9))
SEARCH_MINUTE = int(os.getenv('SEARCH_MINUTE', 0))
BLOG_POST_HOUR = int(os.getenv('BLOG_POST_HOUR', 10))
BLOG_POST_MINUTE = int(os.getenv('BLOG_POST_MINUTE', 0))
FACEBOOK_POST_HOUR = int(os.getenv('FACEBOOK_POST_HOUR', 12))
FACEBOOK_POST_MINUTE = int(os.getenv('FACEBOOK_POST_MINUTE', 0))
INSTAGRAM_POST_HOUR = int(os.getenv('INSTAGRAM_POST_HOUR', 14))
INSTAGRAM_POST_MINUTE = int(os.getenv('INSTAGRAM_POST_MINUTE', 0))

# Other Settings
MAX_ARTICLES_PER_DAY = int(os.getenv('MAX_ARTICLES_PER_DAY', 5))
MIN_ARTICLE_SCORE = float(os.getenv('MIN_ARTICLE_SCORE', 7.0))
DATABASE_PATH = os.getenv('DATABASE_PATH', './data/articles.db')

# Keywords for search
KEYWORDS = [
    # Расчеты и теплопотери
    "расчет воздухообмена в помещении",
    "как рассчитать кратность воздухообмена",
    "расчет теплопотерь через ограждающие конструкции",
    "теплопотери помещения",
    "расчет теплопотерь онлайн",
    "теплопотери расчет",
    "теплопотери в доме",
    "теплопотери через стены",
    
    # Тепловизионное обследование
    "тепловизор теплый пол",
    "видит ли тепловизор через стены",
    "тепловизор для обследования дома",
    "утечка тепла прибор",
    
    # Протечки
    "поиск протечки воды",
    "обнаружение протечек воды",
    "поиск скрытых утечек воды",
    
    # Вентиляция
    "испытания вентиляционных систем",
    "проверка дымогенератором",
    
    # Герметичность
    "проверка на герметичность гост",
    "герметизация помещения",
    "испытания на герметичность трубопроводов",
    
    # Прочее
    "экспертиза домов перед покупкой",
    "энергоэффективность частных домов",
]

# Services descriptions for context
SERVICES = {
    "ventilation_testing": "Испытания герметичности систем вентиляции",
    "thermal_imaging": "Тепловизионное обследование зданий",
    "heat_network_inspection": "Тепловизионное обследование теплотрасс",
    "clean_room_testing": "Проверка герметичности чистых помещений",
    "duct_classification": "Определение классов герметичности воздуховодов",
    "cold_storage_inspection": "Тепловизионное обследование холодильных камер",
    "building_permeability": "Измерение воздухопроницаемости зданий",
    "fire_suppression_testing": "Проверка герметичности при установке газового пожаротушения",
}
