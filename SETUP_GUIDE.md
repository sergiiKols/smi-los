# Подробное руководство по настройке

## Шаг 1: Установка Python

### Windows
1. Скачайте Python 3.8+ с https://www.python.org/downloads/
2. Установите, обязательно отметьте "Add Python to PATH"

### Linux/macOS
```bash
# Проверьте версию Python
python3 --version

# Если нужно, установите
sudo apt-get update
sudo apt-get install python3 python3-pip
```

## Шаг 2: Получение API ключей

### 🔑 Google Gemini API

1. Перейдите на https://makersuite.google.com/
2. Войдите с Google аккаунтом
3. Нажмите "Get API Key"
4. Создайте новый проект или выберите существующий
5. Скопируйте API ключ

**Важно:** Сохраните ключ в безопасном месте

### 🔑 WordPress REST API

#### Способ 1: Пароли приложений (рекомендуется)

1. Войдите в WordPress админку: `https://energo-audit.by/wp-admin`
2. Перейдите: "Пользователи" → "Профиль"
3. Прокрутите до раздела "Пароли приложений"
4. Введите название: "Content Search System"
5. Нажмите "Добавить новый пароль приложения"
6. Скопируйте сгенерированный пароль

**Настройки .env:**
```env
WORDPRESS_URL=https://energo-audit.by
WORDPRESS_USERNAME=ваш_логин
WORDPRESS_PASSWORD=сгенерированный_пароль_приложения
```

#### Способ 2: JWT токен

Если используете JWT плагин:
1. Установите плагин JWT Authentication
2. Настройте согласно документации плагина
3. Адаптируйте код в `wordpress_publisher.py`

### 🔑 Facebook API

#### Шаг 1: Создание приложения

1. Перейдите на https://developers.facebook.com/
2. Нажмите "Мои приложения" → "Создать приложение"
3. Выберите тип "Бизнес"
4. Заполните информацию о приложении

#### Шаг 2: Настройка продуктов

1. Добавьте продукт "Facebook Login"
2. Добавьте продукт "Instagram Graph API"

#### Шаг 3: Получение токена доступа

1. Перейдите в "Инструменты" → "Graph API Explorer"
2. Выберите ваше приложение
3. Выберите страницу Facebook
4. Добавьте разрешения:
   - `pages_read_engagement`
   - `pages_manage_posts`
   - `pages_read_user_content`
5. Нажмите "Generate Access Token"
6. Скопируйте токен

#### Шаг 4: Получение долгосрочного токена

Краткосрочные токены действуют ~1 час. Получите долгосрочный:

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/oauth/access_token?grant_type=fb_exchange_token&client_id=YOUR_APP_ID&client_secret=YOUR_APP_SECRET&fb_exchange_token=YOUR_SHORT_TOKEN"
```

#### Шаг 5: Получение Page ID

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/me/accounts?access_token=YOUR_ACCESS_TOKEN"
```

Найдите ID вашей страницы в ответе.

### 🔑 Instagram API

Instagram использует Facebook Graph API.

#### Шаг 1: Подключение Instagram бизнес-аккаунта

1. Убедитесь, что у вас есть Instagram бизнес-аккаунт
2. Подключите его к Facebook странице
3. В Facebook Developer Console: "Instagram" → "Basic Display"

#### Шаг 2: Получение Business Account ID

```bash
curl -i -X GET "https://graph.facebook.com/v18.0/me/accounts?fields=instagram_business_account&access_token=YOUR_ACCESS_TOKEN"
```

Скопируйте `instagram_business_account.id`

#### Требования для Instagram API:
- Бизнес или Creator аккаунт Instagram
- Подключен к Facebook странице
- Разрешения: `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`

## Шаг 3: Настройка файла .env

Создайте файл `.env` в корне проекта:

```env
# Google Gemini API
GEMINI_API_KEY=AIzaSy...ваш_ключ

# WordPress Configuration
WORDPRESS_URL=https://energo-audit.by
WORDPRESS_USERNAME=admin
WORDPRESS_PASSWORD=xxxx xxxx xxxx xxxx

# Facebook Configuration
FACEBOOK_ACCESS_TOKEN=EAAxxxxxxxxxxxxxxxxxxxxx
FACEBOOK_PAGE_ID=123456789012345

# Instagram Configuration
INSTAGRAM_ACCESS_TOKEN=IGQxxxxxxxxxxxxxxxxxxxxx
INSTAGRAM_BUSINESS_ACCOUNT_ID=17841405309211844

# Scheduling Configuration
SEARCH_HOUR=9
SEARCH_MINUTE=0
BLOG_POST_HOUR=10
BLOG_POST_MINUTE=0
FACEBOOK_POST_HOUR=12
FACEBOOK_POST_MINUTE=0
INSTAGRAM_POST_HOUR=14
INSTAGRAM_POST_MINUTE=0

# Other Settings
MAX_ARTICLES_PER_DAY=5
MIN_ARTICLE_SCORE=7.0
DATABASE_PATH=./data/articles.db
```

## Шаг 4: Тестирование

### Тест 1: Проверка конфигурации

```bash
python main.py --mode test
```

### Тест 2: Проверка поиска

```bash
python main.py --mode test --test-keyword "тепловизор"
```

### Тест 3: Проверка WordPress

Создайте тестовый файл `test_wordpress.py`:

```python
from wordpress_publisher import WordPressPublisher

wp = WordPressPublisher()

post_data = {
    'title': 'Тестовый пост',
    'content': '<p>Это тестовый пост для проверки API</p>',
    'status': 'draft'
}

post_id = wp.create_post(post_data)
print(f"Post created: {post_id}")
```

Запустите:
```bash
python test_wordpress.py
```

### Тест 4: Проверка Facebook

Создайте файл `test_facebook.py`:

```python
from social_media_publisher import FacebookPublisher

fb = FacebookPublisher()
post_id = fb.create_post("Тестовый пост от системы автоматизации")
print(f"Facebook post created: {post_id}")
```

Запустите:
```bash
python test_facebook.py
```

## Шаг 5: Первый запуск

### Ручной запуск для тестирования

```bash
# 1. Запустите поиск статей
python main.py --mode search

# 2. Проверьте найденные статьи
sqlite3 data/articles.db "SELECT title, ai_score FROM articles ORDER BY ai_score DESC LIMIT 5;"

# 3. Опубликуйте на блоге
python main.py --mode publish-blog

# 4. Проверьте результаты в WordPress админке
```

### Запуск планировщика

```bash
python main.py --mode scheduler
```

Система будет работать постоянно и выполнять задачи по расписанию.

## Шаг 6: Автозапуск (опционально)

### Для Linux (Ubuntu/Debian)

1. Создайте systemd service:

```bash
sudo nano /etc/systemd/system/content-search.service
```

2. Вставьте:

```ini
[Unit]
Description=Content Search and Publishing System
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/home/your_username/content-search-system
ExecStart=/usr/bin/python3 /home/your_username/content-search-system/main.py --mode scheduler
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

3. Активируйте:

```bash
sudo systemctl daemon-reload
sudo systemctl enable content-search
sudo systemctl start content-search
sudo systemctl status content-search
```

### Для Windows

1. Используйте Task Scheduler:
   - Откройте Task Scheduler
   - "Создать задачу"
   - Триггер: "При входе в систему"
   - Действие: запустить `python main.py --mode scheduler`

2. Или установите как службу с помощью NSSM:

```bash
nssm install ContentSearch "C:\Python39\python.exe" "C:\path\to\main.py --mode scheduler"
nssm start ContentSearch
```

## Решение проблем

### Ошибка: "ModuleNotFoundError"

```bash
pip install -r requirements.txt
```

### Ошибка: "Authentication failed" (WordPress)

- Проверьте правильность логина и пароля
- Убедитесь, что REST API включен в WordPress
- Проверьте, что у пользователя есть права на создание постов

### Ошибка: "Invalid access token" (Facebook)

- Токен истек - получите новый долгосрочный токен
- Проверьте разрешения токена
- Убедитесь, что Page ID правильный

### Ошибка: Gemini API не отвечает

- Проверьте API ключ
- Проверьте квоты и лимиты в Google Cloud Console
- Убедитесь в наличии интернет-соединения

### База данных не создается

```bash
mkdir -p data logs
chmod 755 data logs
```

## Мониторинг работы

### Просмотр логов

```bash
# Linux
tail -f logs/system.log

# Windows
Get-Content logs\system.log -Wait
```

### Проверка статистики

```bash
# Сколько статей найдено
sqlite3 data/articles.db "SELECT COUNT(*) FROM articles;"

# Статистика по платформам
sqlite3 data/articles.db "SELECT platform, COUNT(*) FROM publications GROUP BY platform;"

# Топ ключевых слов
sqlite3 data/articles.db "SELECT keyword, SUM(results_count) as total FROM search_history GROUP BY keyword ORDER BY total DESC LIMIT 10;"
```

## Оптимизация и настройка

### Изменение частоты поиска

В `.env` или `config.py` можно настроить количество результатов:

```python
# В gemini_search.py, метод search_articles
articles = self.gemini.search_articles(keyword, num_results=10)  # Измените число
```

### Настройка критериев оценки

В `gemini_search.py` адаптируйте промпты для анализа статей под ваши критерии.

### Добавление новых источников

Создайте дополнительные модули для парсинга RSS, новостных сайтов и т.д.

---

**Готово!** Ваша система настроена и готова к работе.

При возникновении вопросов обращайтесь к README.md или документации API.
