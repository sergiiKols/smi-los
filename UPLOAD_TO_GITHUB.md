# 📦 Загрузка проекта на GitHub

## Ваш репозиторий: https://github.com/sergiiKols/smi

---

## 🚀 КОМАНДЫ ДЛЯ ЗАГРУЗКИ

Выполните эти команды в корневой директории проекта:

### Шаг 1: Инициализация Git (если еще не сделано)

```bash
git init
```

### Шаг 2: Добавьте все файлы

```bash
git add .
```

### Шаг 3: Проверьте что добавлено (опционально)

```bash
git status
```

**Убедитесь что .env файл НЕ в списке!** Он должен быть в .gitignore.

### Шаг 4: Создайте первый коммит

```bash
git commit -m "Initial commit: Content Search System with Web Dashboard

Features:
- Python automation system for article search and publishing
- Gemini API integration for AI-powered content analysis
- WordPress, Facebook, Instagram publishers
- Next.js web dashboard for content management
- FastAPI backend server
- Complete documentation (11 files)
- Ready for Vercel deployment"
```

### Шаг 5: Подключите удаленный репозиторий

```bash
git remote add origin https://github.com/sergiiKols/smi.git
```

### Шаг 6: Переименуйте ветку в main (если нужно)

```bash
git branch -M main
```

### Шаг 7: Загрузите код на GitHub

```bash
git push -u origin main
```

---

## 🔐 Аутентификация

При первом push GitHub может запросить аутентификацию.

### Вариант 1: Personal Access Token (рекомендуется)

1. Зайдите на GitHub: https://github.com/settings/tokens
2. Нажмите "Generate new token" → "Generate new token (classic)"
3. Выберите scopes: `repo` (полный доступ к репозиториям)
4. Нажмите "Generate token"
5. **Скопируйте токен** (он больше не покажется!)
6. При push используйте токен как пароль:
   - Username: `sergiiKols`
   - Password: `ваш_токен`

### Вариант 2: SSH ключ

```bash
# Генерация SSH ключа
ssh-keygen -t ed25519 -C "your_email@example.com"

# Копирование публичного ключа
cat ~/.ssh/id_ed25519.pub

# Добавьте ключ на GitHub:
# Settings → SSH and GPG keys → New SSH key

# Измените URL на SSH
git remote set-url origin git@github.com:sergiiKols/smi.git

# Push
git push -u origin main
```

---

## ✅ ПРОВЕРКА

После успешной загрузки:

1. Откройте: https://github.com/sergiiKols/smi
2. Проверьте что все файлы загружены
3. Убедитесь что файл `.env` **НЕ** в репозитории

---

## 📝 ВСЕ КОМАНДЫ ОДНОЙ СТРОКОЙ

Для быстрой загрузки (если Git уже инициализирован):

```bash
git add . && git commit -m "Initial commit: Content Search System" && git remote add origin https://github.com/sergiiKols/smi.git && git branch -M main && git push -u origin main
```

---

## 🔄 ОБНОВЛЕНИЕ КОДА (в будущем)

После внесения изменений:

```bash
git add .
git commit -m "Описание изменений"
git push
```

---

## 🐛 Решение проблем

### Ошибка: "remote origin already exists"

```bash
git remote remove origin
git remote add origin https://github.com/sergiiKols/smi.git
```

### Ошибка: "failed to push some refs"

```bash
# Если репозиторий не пустой на GitHub
git pull origin main --allow-unrelated-histories
git push -u origin main
```

### Проверка подключенного репозитория

```bash
git remote -v
```

Должно показать:
```
origin  https://github.com/sergiiKols/smi.git (fetch)
origin  https://github.com/sergiiKols/smi.git (push)
```

---

## 📊 ПОСЛЕ ЗАГРУЗКИ

### Следующие шаги:

1. ✅ Код на GitHub
2. 🚀 Деплой frontend на Vercel (см. DEPLOYMENT.md)
3. 🔧 Деплой backend на Railway (см. DEPLOYMENT.md)
4. ⚙️ Настройка переменных окружения
5. 🎉 Готово!

---

**Готово к загрузке!** 🚀
