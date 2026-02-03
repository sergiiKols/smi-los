# 🚀 Руководство по развертыванию

Полное руководство по развертыванию системы автоматического поиска и публикации контента на GitHub и Vercel.

## 📋 Содержание

1. [Подготовка к развертыванию](#подготовка)
2. [Развертывание на GitHub](#github)
3. [Развертывание Frontend на Vercel](#vercel-frontend)
4. [Развертывание Backend API](#backend)
5. [Подключение компонентов](#подключение)
6. [Настройка автозапуска](#автозапуск)

---

## 1. Подготовка к развертыванию {#подготовка}

### Проверьте наличие всех файлов

```bash
# Основная система
ls -la *.py
ls -la requirements.txt
ls -la .env.example

# Web интерфейс
ls -la web/
ls -la web/package.json
ls -la web/vercel.json

# API сервер
ls -la api_server.py
ls -la api_requirements.txt
```

### Создайте .env файл

```bash
cp .env.example .env
# Отредактируйте .env с вашими API ключами
```

### Проверьте работоспособность локально

```bash
# Тест основной системы
python main.py --mode test

# Тест API сервера
python api_server.py &
curl http://localhost:3001/

# Тест веб-интерфейса
cd web
npm install
npm run dev
```

---

## 2. Развертывание на GitHub {#github}

### Шаг 1: Создайте репозиторий на GitHub

1. Зайдите на https://github.com
2. Нажмите "New repository"
3. Название: `content-search-system` (или другое)
4. Выберите Public или Private
5. НЕ добавляйте README, .gitignore (уже есть)
6. Нажмите "Create repository"

### Шаг 2: Инициализируйте Git локально

```bash
# Инициализация
git init

# Добавьте все файлы
git add .

# Первый коммит
git commit -m "Initial commit: Content Search System with Web Dashboard"

# Подключите удаленный репозиторий
git remote add origin https://github.com/ваш-username/content-search-system.git

# Переименуйте ветку в main (если нужно)
git branch -M main

# Push на GitHub
git push -u origin main
```

### Шаг 3: Проверьте на GitHub

Откройте ваш репозиторий на GitHub и убедитесь, что все файлы загружены.

### ⚠️ Важно: Безопасность

Убедитесь, что файл `.env` в `.gitignore`:

```bash
cat .gitignore | grep .env
```

Если его там нет, добавьте:

```bash
echo ".env" >> .gitignore
git add .gitignore
git commit -m "Add .env to gitignore"
git push
```

---

## 3. Развертывание Frontend на Vercel {#vercel-frontend}

### Способ A: Через Vercel Dashboard (рекомендуется)

#### Шаг 1: Создайте аккаунт на Vercel

1. Зайдите на https://vercel.com
2. Нажмите "Sign Up"
3. Войдите через GitHub

#### Шаг 2: Импортируйте проект

1. Нажмите "Add New..." → "Project"
2. Выберите ваш репозиторий `content-search-system`
3. Нажмите "Import"

#### Шаг 3: Настройте проект

**Framework Preset:** Next.js

**Root Directory:** `web`

**Build Command:** `npm run build`

**Output Directory:** `.next`

**Install Command:** `npm install`

#### Шаг 4: Настройте переменные окружения

В разделе "Environment Variables" добавьте:

```
API_BASE_URL = https://your-api-server.com
```

(Замените на реальный URL вашего API после развертывания backend)

#### Шаг 5: Deploy

Нажмите "Deploy" и дождитесь завершения.

Ваш сайт будет доступен на: `https://your-project.vercel.app`

### Способ B: Через Vercel CLI

```bash
# Установите Vercel CLI
npm install -g vercel

# Войдите
vercel login

# Перейдите в директорию web
cd web

# Деплой
vercel

# Для продакшн деплоя
vercel --prod
```

### Настройка кастомного домена (опционально)

1. В настройках проекта → "Domains"
2. Добавьте ваш домен (например, `dashboard.energo-audit.by`)
3. Настройте DNS записи согласно инструкциям Vercel

---

## 4. Развертывание Backend API {#backend}

У вас есть несколько вариантов для развертывания Python API:

### Вариант A: Railway.app (рекомендуется)

#### Шаг 1: Создайте аккаунт

Зайдите на https://railway.app и зарегистрируйтесь через GitHub.

#### Шаг 2: Создайте новый проект

1. Нажмите "New Project"
2. Выберите "Deploy from GitHub repo"
3. Выберите ваш репозиторий

#### Шаг 3: Настройте

**Start Command:**
```bash
python api_server.py
```

**Environment Variables:**
Добавьте все переменные из вашего `.env` файла:
```
GEMINI_API_KEY=...
WORDPRESS_URL=...
WORDPRESS_USERNAME=...
WORDPRESS_PASSWORD=...
FACEBOOK_ACCESS_TOKEN=...
FACEBOOK_PAGE_ID=...
INSTAGRAM_ACCESS_TOKEN=...
INSTAGRAM_BUSINESS_ACCOUNT_ID=...
```

#### Шаг 4: Deploy

Railway автоматически развернет проект.

Получите URL: `https://ваш-проект.up.railway.app`

### Вариант B: Render.com

1. Зайдите на https://render.com
2. "New" → "Web Service"
3. Подключите GitHub репозиторий
4. **Build Command:** `pip install -r api_requirements.txt`
5. **Start Command:** `python api_server.py`
6. Добавьте Environment Variables
7. Deploy

### Вариант C: Heroku

```bash
# Создайте Procfile
echo "web: python api_server.py" > Procfile

# Создайте runtime.txt
echo "python-3.9.18" > runtime.txt

# Деплой
heroku login
heroku create your-app-name
git push heroku main
heroku config:set GEMINI_API_KEY=your-key
# ... добавьте остальные переменные
```

### Вариант D: Собственный VPS/сервер

```bash
# На сервере
git clone https://github.com/ваш-username/content-search-system.git
cd content-search-system

# Установите зависимости
pip install -r api_requirements.txt

# Создайте .env файл
cp .env.example .env
nano .env  # Добавьте ваши ключи

# Запустите с помощью systemd
sudo nano /etc/systemd/system/content-api.service
```

Содержимое `content-api.service`:
```ini
[Unit]
Description=Content Search API Server
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/content-search-system
ExecStart=/usr/bin/python3 api_server.py
Restart=always

[Install]
WantedBy=multi-user.target
```

```bash
# Активируйте
sudo systemctl enable content-api
sudo systemctl start content-api
```

---

## 5. Подключение компонентов {#подключение}

### Шаг 1: Обновите API_BASE_URL на Vercel

После развертывания API, обновите переменную окружения на Vercel:

1. Зайдите в настройки проекта на Vercel
2. "Settings" → "Environment Variables"
3. Измените `API_BASE_URL` на URL вашего API:
   ```
   API_BASE_URL=https://your-api.railway.app
   ```
4. Redeploy проект

### Шаг 2: Настройте CORS на API

В `api_server.py` обновите CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-project.vercel.app",
        "http://localhost:3000"  # для разработки
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

Commit и push изменения:
```bash
git add api_server.py
git commit -m "Update CORS settings"
git push
```

### Шаг 3: Проверьте подключение

Откройте ваш dashboard на Vercel и проверьте:
- Загружается ли статистика
- Работают ли кнопки действий
- Отображаются ли статьи

---

## 6. Настройка автозапуска основной системы {#автозапуск}

Основная система поиска и публикации должна работать постоянно на сервере.

### На Linux сервере (systemd)

```bash
sudo nano /etc/systemd/system/content-search.service
```

Содержимое:
```ini
[Unit]
Description=Content Search and Publishing System
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/content-search-system
ExecStart=/usr/bin/python3 main.py --mode scheduler
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активация:
```bash
sudo systemctl enable content-search
sudo systemctl start content-search
sudo systemctl status content-search
```

### На Windows (Task Scheduler)

1. Откройте Task Scheduler
2. "Create Basic Task"
3. Name: "Content Search System"
4. Trigger: "When the computer starts"
5. Action: "Start a program"
6. Program: `C:\Python39\python.exe`
7. Arguments: `C:\path\to\main.py --mode scheduler`
8. Finish

### Альтернатива: Cron (для периодического запуска)

```bash
crontab -e

# Добавьте строки
0 9 * * * cd /path/to/content-search-system && python3 main.py --mode search
0 10 * * * cd /path/to/content-search-system && python3 main.py --mode publish-blog
0 12 * * * cd /path/to/content-search-system && python3 main.py --mode publish-social
```

---

## ✅ Проверка развертывания

### Чеклист

- [ ] Код загружен на GitHub
- [ ] Frontend развернут на Vercel
- [ ] Backend API развернут и доступен
- [ ] API_BASE_URL настроен на Vercel
- [ ] CORS настроен на API
- [ ] Переменные окружения заданы
- [ ] Dashboard открывается и показывает данные
- [ ] Основная система запущена на сервере
- [ ] Логи работают корректно

### Тестирование

1. **Frontend:**
   - Откройте https://your-project.vercel.app
   - Проверьте все страницы
   - Проверьте статистику

2. **API:**
   - Откройте https://your-api.railway.app
   - Проверьте https://your-api.railway.app/api/stats

3. **Основная система:**
   - Проверьте логи: `sudo journalctl -u content-search -f`
   - Проверьте базу данных: `sqlite3 data/articles.db "SELECT COUNT(*) FROM articles;"`

---

## 🔄 Обновления

### Обновление кода

```bash
# Локально внесите изменения
git add .
git commit -m "Update: описание изменений"
git push

# Vercel автоматически пересоберет frontend
# Railway/Render автоматически пересоберут backend
```

### Ручное обновление на сервере

```bash
cd /path/to/content-search-system
git pull origin main
sudo systemctl restart content-search
```

---

## 🐛 Troubleshooting

### Dashboard не показывает данные

1. Проверьте API URL в переменных Vercel
2. Проверьте что API отвечает: `curl https://your-api.railway.app/api/stats`
3. Проверьте CORS настройки

### API возвращает ошибки

1. Проверьте логи на Railway/Render
2. Проверьте переменные окружения
3. Проверьте что база данных существует

### Основная система не работает

1. Проверьте статус: `sudo systemctl status content-search`
2. Проверьте логи: `sudo journalctl -u content-search -f`
3. Проверьте .env файл

---

## 📞 Поддержка

Если возникли проблемы:
1. Проверьте логи на каждом компоненте
2. Создайте issue на GitHub
3. Свяжитесь с разработчиком

---

**Готово! Ваша система полностью развернута и работает! 🎉**
