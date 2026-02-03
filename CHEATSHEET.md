# 🚀 ШПАРГАЛКА - Быстрый старт

## 1️⃣ ЛОКАЛЬНЫЙ ЗАПУСК (5 минут)

### Основная система:
```bash
pip install -r requirements.txt
cp .env.example .env
# Отредактируйте .env
python main.py --mode test
```

### Веб-интерфейс:
```bash
cd web
npm install
npm run dev
```

### API сервер:
```bash
pip install -r api_requirements.txt
python api_server.py
```

Откройте: http://localhost:3000

---

## 2️⃣ ДЕПЛОЙ НА GITHUB + VERCEL (10 минут)

### GitHub:
```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/username/repo.git
git push -u origin main
```

### Vercel:
1. Зайдите на vercel.com
2. Import repository
3. Root Directory: web
4. Deploy

### Backend API (Railway):
1. Зайдите на railway.app
2. New Project → Deploy from GitHub
3. Start command: python api_server.py
4. Добавьте environment variables

---

## 3️⃣ НЕОБХОДИМЫЕ API КЛЮЧИ

✅ Google Gemini API → https://makersuite.google.com/app/apikey
✅ WordPress → username + app password
✅ Facebook → Access Token + Page ID
✅ Instagram → Access Token + Business Account ID

Подробно: SETUP_GUIDE.md

---

## 4️⃣ СТРУКТУРА ПРОЕКТА

content-search-system/
├── main.py              # Точка входа
├── api_server.py        # Backend API
├── web/                 # Frontend Next.js
│   ├── app/            # Страницы
│   └── components/     # Компоненты
└── *.md                # Документация

---

## 5️⃣ ОСНОВНЫЕ КОМАНДЫ

### Режимы работы:
```bash
python main.py --mode scheduler      # Полная автоматизация
python main.py --mode search         # Только поиск
python main.py --mode publish-blog   # Только публикация
python main.py --mode test           # Тестирование
```

### Веб-интерфейс:
```bash
cd web
npm run dev      # Разработка
npm run build    # Сборка
npm run start    # Продакшн
```

---

## 6️⃣ ПОЛЕЗНЫЕ ССЫЛКИ

📖 README.md - Полное руководство
⚡ QUICKSTART.md - Быстрый старт
🔧 SETUP_GUIDE.md - Настройка API
🚀 DEPLOYMENT.md - Деплой
📦 GITHUB_SETUP.md - GitHub
🌐 WEB_DEPLOYMENT_SUMMARY.md - Веб-часть
📊 COMPLETE_PROJECT_SUMMARY.md - Полная сводка

---

## 💡 ПОМОЩЬ

Проблемы? Читайте документацию в корне проекта!

Все готово! Удачи! 🎉
