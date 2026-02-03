# 📦 Инструкция по загрузке на GitHub

## Шаг 1: Подготовка

### Проверьте .gitignore

Убедитесь, что файл `.gitignore` содержит:

```
# Environment
.env
.env.local

# Python
__pycache__/
*.pyc
data/
*.db

# Node
node_modules/
.next/

# Vercel
.vercel/
```

### Проверьте структуру проекта

```bash
ls -la
```

Должны быть:
- Python файлы (main.py, config.py, и т.д.)
- Директория `web/` с Next.js проектом
- Файлы документации (README.md, DEPLOYMENT.md)

## Шаг 2: Инициализация Git

```bash
# Инициализируйте репозиторий
git init

# Проверьте статус
git status

# Добавьте все файлы
git add .

# Проверьте что .env НЕ добавлен
git status | grep .env

# Если .env в списке, удалите его
git reset HEAD .env
echo ".env" >> .gitignore
```

## Шаг 3: Первый коммит

```bash
git commit -m "Initial commit: Content Search System with Web Dashboard

- Python automation system for article search and publishing
- Gemini API integration for AI-powered search
- WordPress, Facebook, Instagram publishers
- Next.js web dashboard for management
- Complete documentation"
```

## Шаг 4: Создайте репозиторий на GitHub

1. Зайдите на https://github.com
2. Нажмите "+" в правом верхнем углу → "New repository"
3. Заполните:
   - **Repository name:** `content-search-system`
   - **Description:** "Automated content search and publishing system with AI analysis"
   - **Public** или **Private** (на ваш выбор)
   - НЕ добавляйте README, .gitignore, license (уже есть)
4. Нажмите "Create repository"

## Шаг 5: Подключите удаленный репозиторий

GitHub покажет инструкции. Выполните:

```bash
# Добавьте удаленный репозиторий
git remote add origin https://github.com/ВАШ_USERNAME/content-search-system.git

# Переименуйте ветку в main (если нужно)
git branch -M main

# Загрузите код
git push -u origin main
```

### Если требуется аутентификация

**Вариант 1: SSH (рекомендуется)**

```bash
# Сгенерируйте SSH ключ
ssh-keygen -t ed25519 -C "your_email@example.com"

# Скопируйте публичный ключ
cat ~/.ssh/id_ed25519.pub

# Добавьте ключ на GitHub:
# Settings → SSH and GPG keys → New SSH key

# Измените URL на SSH
git remote set-url origin git@github.com:ВАШ_USERNAME/content-search-system.git

# Push
git push -u origin main
```

**Вариант 2: Personal Access Token**

```bash
# Создайте токен на GitHub:
# Settings → Developer settings → Personal access tokens → Generate new token

# При push используйте токен вместо пароля
git push -u origin main
# Username: ваш_username
# Password: ваш_токен
```

## Шаг 6: Проверьте на GitHub

Откройте https://github.com/ВАШ_USERNAME/content-search-system

Проверьте что загружены:
- ✅ Все Python файлы
- ✅ Директория web/
- ✅ Документация (README.md, DEPLOYMENT.md)
- ✅ .gitignore
- ❌ НЕТ файла .env (он должен быть скрыт)

## Шаг 7: Настройте описание репозитория

На странице репозитория:
1. Нажмите ⚙️ справа от "About"
2. Добавьте описание:
   ```
   🤖 Automated content search and publishing system with AI analysis for energo-audit.by
   ```
3. Добавьте теги:
   ```
   python, nextjs, ai, automation, gemini-api, wordpress, content-management
   ```
4. Сохраните

## Шаг 8: Создайте README badge (опционально)

Добавьте в начало README.md:

```markdown
[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/ВАШ_USERNAME/content-search-system/tree/main/web)
```

Коммит и push:
```bash
git add README.md
git commit -m "Add Vercel deploy button"
git push
```

## 📝 Регулярные обновления

### Внесение изменений

```bash
# Внесите изменения в файлы
git add .
git commit -m "Описание изменений"
git push
```

### Хорошие практики коммитов

```bash
# Добавление функционала
git commit -m "feat: Add image generation for Instagram"

# Исправление бага
git commit -m "fix: Correct API CORS settings"

# Обновление документации
git commit -m "docs: Update deployment guide"

# Рефакторинг
git commit -m "refactor: Improve database queries"
```

## 🔒 Безопасность

### Никогда не коммитьте:
- ❌ Файл .env с API ключами
- ❌ Базу данных с реальными данными
- ❌ Пароли и токены
- ❌ Приватные ключи

### Что делать если случайно закоммитили .env:

```bash
# Удалите файл из истории
git rm --cached .env

# Добавьте в .gitignore
echo ".env" >> .gitignore

# Коммит
git add .gitignore
git commit -m "Remove .env from tracking"
git push --force

# ВАЖНО: Смените все API ключи!
```

## 🌟 Рекомендации

### Создайте branches для разработки

```bash
# Создайте ветку для новой функции
git checkout -b feature/new-feature

# Внесите изменения
git add .
git commit -m "Add new feature"

# Push ветки
git push origin feature/new-feature

# На GitHub создайте Pull Request
```

### Настройте GitHub Actions

Файл `.github/workflows/deploy.yml` уже создан для автоматического деплоя.

Добавьте secrets на GitHub:
1. Settings → Secrets and variables → Actions
2. Добавьте:
   - `VERCEL_TOKEN`
   - `VERCEL_ORG_ID`
   - `VERCEL_PROJECT_ID`
   - `API_BASE_URL`

## ✅ Готово!

Ваш код теперь на GitHub и готов к деплою на Vercel.

**Следующий шаг:** См. DEPLOYMENT.md для инструкций по развертыванию.
