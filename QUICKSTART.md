# 🚀 Быстрый старт

## За 5 минут до запуска

### 1. Установите зависимости

```bash
pip install -r requirements.txt
```

### 2. Настройте конфигурацию

```bash
cp .env.example .env
nano .env  # или любой текстовый редактор
```

Минимальная конфигурация для начала:

```env
GEMINI_API_KEY=ваш_ключ_gemini
WORDPRESS_URL=https://energo-audit.by
WORDPRESS_USERNAME=admin
WORDPRESS_PASSWORD=ваш_пароль
```

### 3. Тестовый запуск

```bash
python main.py --mode test
```

### 4. Запустите поиск

```bash
python main.py --mode search
```

### 5. Проверьте результаты

```bash
python -c "from database import ArticleDatabase; db = ArticleDatabase(); print(f'Найдено статей: {len(db.get_pending_articles())}')"
```

## Готово! 🎉

Теперь можете:

- **Запустить полную систему:** `python main.py --mode scheduler`
- **Опубликовать в блог:** `python main.py --mode publish-blog`
- **Опубликовать в соцсети:** `python main.py --mode publish-social`

---

## Альтернативный запуск

### Linux/macOS
```bash
chmod +x run.sh
./run.sh scheduler
```

### Windows
```bash
run.bat scheduler
```

---

## Что делает система?

1. ⏰ **09:00** - Ищет статьи по вашим ключевым словам
2. 🤖 **AI анализирует** - Оценивает качество и релевантность
3. 📝 **10:00** - Публикует лучшие статьи на блог
4. 📱 **12:00** - Публикует в Facebook
5. 📸 **14:00** - Публикует в Instagram

---

## Настройка расписания

Измените время в `.env`:

```env
SEARCH_HOUR=9
BLOG_POST_HOUR=10
FACEBOOK_POST_HOUR=12
INSTAGRAM_POST_HOUR=14
```

---

## Важно знать

⚠️ **WordPress посты создаются как черновики** - измените `status='draft'` на `status='publish'` в `scheduler.py` (строка 116) для автопубликации

⚠️ **Instagram требует изображения** - добавьте логику генерации/подбора изображений

⚠️ **API лимиты** - следите за квотами Gemini API

---

## Мониторинг

### Просмотр найденных статей

```bash
sqlite3 data/articles.db "SELECT title, ai_score FROM articles ORDER BY ai_score DESC LIMIT 10;"
```

### Статистика публикаций

```bash
sqlite3 data/articles.db "SELECT platform, COUNT(*) as count FROM publications GROUP BY platform;"
```

### Логи

```bash
tail -f logs/system.log  # Linux
Get-Content logs\system.log -Wait  # Windows
```

---

## Нужна помощь?

📖 Подробная документация: **[README.md](README.md)**  
🔧 Руководство по настройке: **[SETUP_GUIDE.md](SETUP_GUIDE.md)**  
⚙️ Конфигурация проекта: **[project_config.md](project_config.md)**

---

**Удачи! 🚀**
