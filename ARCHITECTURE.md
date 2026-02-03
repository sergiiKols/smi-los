# 🏗️ Архитектура системы

## Обзор

Система автоматического поиска и публикации контента состоит из нескольких взаимодействующих модулей.

```
┌─────────────────────────────────────────────────────────────┐
│                        SCHEDULER                             │
│                     (scheduler.py)                           │
│  Управляет расписанием и координирует все модули             │
└─────────────────────────────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        ▼                   ▼                   ▼
┌──────────────┐   ┌──────────────┐   ┌──────────────┐
│   SEARCH     │   │   ANALYSIS   │   │  PUBLISHING  │
│ (gemini)     │──▶│   (gemini)   │──▶│  (wp, social)│
└──────────────┘   └──────────────┘   └──────────────┘
        │                   │                   │
        └───────────────────┴───────────────────┘
                            ▼
                   ┌──────────────┐
                   │   DATABASE   │
                   │  (SQLite)    │
                   └──────────────┘
```

## Компоненты системы

### 1. **main.py** - Точка входа
- Парсинг аргументов командной строки
- Инициализация системы
- Выбор режима работы

### 2. **config.py** - Конфигурация
- Загрузка переменных окружения
- Определение ключевых слов
- Настройки расписания
- Константы системы

### 3. **database.py** - База данных
Управление SQLite базой данных:
- **Таблица `articles`**: хранение найденных статей
- **Таблица `publications`**: история публикаций
- **Таблица `search_history`**: история поиска

#### Схема базы данных

```sql
articles
├── id (INTEGER PRIMARY KEY)
├── title (TEXT)
├── url (TEXT UNIQUE)
├── content (TEXT)
├── source (TEXT)
├── keywords (TEXT JSON)
├── ai_score (REAL)
├── relevance_score (REAL)
├── found_date (TIMESTAMP)
├── status (TEXT)
└── analysis (TEXT JSON)

publications
├── id (INTEGER PRIMARY KEY)
├── article_id (INTEGER FK)
├── platform (TEXT)
├── post_id (TEXT)
├── published_date (TIMESTAMP)
└── status (TEXT)

search_history
├── id (INTEGER PRIMARY KEY)
├── keyword (TEXT)
├── search_date (TIMESTAMP)
└── results_count (INTEGER)
```

### 4. **gemini_search.py** - Поиск и анализ через Gemini

#### Класс: `GeminiSearchEngine`

**Методы:**

- `search_articles(keyword, num_results)`: Поиск статей по ключевому слову
- `analyze_article(article)`: Анализ качества и релевантности статьи
- `generate_blog_post(article)`: Генерация оптимизированного поста для блога

**Процесс анализа:**

```python
article → analyze_article() → {
    scores: {
        relevance: 0-10,
        quality: 0-10,
        timeliness: 0-10,
        business_value: 0-10,
        uniqueness: 0-10,
        overall: 0-10
    },
    key_topics: [...],
    target_audience: "...",
    adaptation_tips: "...",
    social_media_title: "..."
}
```

### 5. **wordpress_publisher.py** - Публикация в WordPress

#### Класс: `WordPressPublisher`

**Методы:**

- `create_post(post_data)`: Создание нового поста
- `update_post(post_id, post_data)`: Обновление существующего поста
- `format_blog_post(blog_data)`: Форматирование контента в HTML
- `_get_or_create_tags(tag_names)`: Управление тегами

**Работа с WordPress REST API:**

```
POST /wp-json/wp/v2/posts
Authorization: Basic (username:password)
Content-Type: application/json

{
    "title": "...",
    "content": "...",
    "status": "draft|publish",
    "tags": [id1, id2],
    "categories": [id1]
}
```

### 6. **social_media_publisher.py** - Публикация в соцсети

#### Класс: `FacebookPublisher`

**Методы:**

- `create_post(message, link)`: Создание текстового поста
- `create_photo_post(message, image_url)`: Создание поста с изображением
- `format_post_message(article, blog_url)`: Форматирование сообщения

#### Класс: `InstagramPublisher`

**Методы:**

- `create_post(image_url, caption)`: Создание поста (требует изображение)
- `format_post_caption(article)`: Форматирование подписи

**Процесс публикации в Instagram:**

```
1. Create Media Container
   POST /instagram_account_id/media
   
2. Publish Media
   POST /instagram_account_id/media_publish
```

#### Класс: `SocialMediaManager`

Координирует публикацию на всех платформах:

```python
publish_to_all(article, blog_url, image_url) → {
    'facebook': post_id,
    'instagram': media_id
}
```

### 7. **scheduler.py** - Планировщик задач

#### Класс: `ContentScheduler`

**Основные задачи:**

1. **search_and_collect_articles()** - Поиск статей
   - Проходит по всем ключевым словам
   - Использует Gemini для поиска
   - Анализирует качество
   - Сохраняет в базу данных

2. **publish_to_blog()** - Публикация на блог
   - Выбирает топ статьи из базы
   - Генерирует оптимизированный контент
   - Публикует в WordPress
   - Обновляет статусы

3. **publish_to_facebook()** - Публикация в Facebook
   - Форматирует сообщение
   - Добавляет ссылку на блог
   - Публикует

4. **publish_to_instagram()** - Публикация в Instagram
   - Требует изображение
   - Форматирует подпись
   - Публикует

## Поток данных

### 1. Ежедневный поиск (09:00)

```
Scheduler → GeminiSearch
    ↓
Для каждого ключевого слова:
    ↓
GeminiSearch.search_articles()
    ↓
Для каждой найденной статьи:
    ↓
GeminiSearch.analyze_article()
    ↓
Database.add_article()
    ↓
Database.add_search_history()
```

### 2. Публикация в блог (10:00)

```
Scheduler → Database.get_pending_articles()
    ↓
Для каждой статьи (топ 5):
    ↓
GeminiSearch.generate_blog_post()
    ↓
WordPressPublisher.format_blog_post()
    ↓
WordPressPublisher.create_post()
    ↓
Database.update_article_status()
    ↓
Database.add_publication()
```

### 3. Публикация в соцсети (12:00, 14:00)

```
Scheduler → Database.get_pending_articles()
    ↓
SocialMediaManager.publish_to_all()
    ↓
    ├─▶ FacebookPublisher.create_post()
    │       ↓
    │   Database.add_publication('facebook')
    │
    └─▶ InstagramPublisher.create_post()
            ↓
        Database.add_publication('instagram')
```

## Режимы работы

### Scheduler Mode (основной)
```bash
python main.py --mode scheduler
```
Непрерывная работа с выполнением всех задач по расписанию.

### Search Mode
```bash
python main.py --mode search
```
Однократный запуск поиска статей.

### Publish Blog Mode
```bash
python main.py --mode publish-blog
```
Однократная публикация в WordPress.

### Publish Social Mode
```bash
python main.py --mode publish-social
```
Однократная публикация в соцсети.

### Test Mode
```bash
python main.py --mode test --test-keyword "ключевое слово"
```
Тестирование поиска без сохранения в базу.

## Обработка ошибок

Каждый модуль содержит обработку ошибок:

1. **Логирование** - все действия логируются
2. **Try-Catch блоки** - перехват исключений
3. **Валидация** - проверка данных перед обработкой
4. **Откат** - сохранение состояния при ошибках

## Масштабирование

### Горизонтальное

- Запуск нескольких инстансов для разных групп ключевых слов
- Использование очереди задач (Celery, RabbitMQ)

### Вертикальное

- Кэширование результатов Gemini
- Оптимизация запросов к базе данных
- Асинхронные операции (async/await)

## Безопасность

1. **API ключи** - хранятся в `.env`, не коммитятся в Git
2. **Аутентификация** - использование токенов и паролей приложений
3. **Rate limiting** - задержки между запросами к API
4. **Валидация** - проверка всех входных данных

## Мониторинг

- **Логи** - все действия записываются в логи
- **База данных** - статистика в таблицах
- **Метрики** - количество найденных/опубликованных статей

## Расширение системы

### Добавление новых источников

Создайте новый модуль, например `rss_parser.py`:

```python
class RSSParser:
    def search_articles(self, feed_url):
        # Парсинг RSS
        pass
```

### Добавление новых платформ

Расширьте `social_media_publisher.py`:

```python
class TelegramPublisher:
    def create_post(self, message):
        # Публикация в Telegram
        pass
```

### Добавление новой логики анализа

Модифицируйте промпты в `gemini_search.py` или добавьте дополнительные метрики.

---

**Архитектура спроектирована для:**
- Модульности
- Расширяемости
- Надежности
- Простоты поддержки
