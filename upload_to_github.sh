#!/bin/bash

echo "========================================"
echo "  ЗАГРУЗКА НА GITHUB"
echo "  Repository: sergiiKols/smi"
echo "========================================"
echo ""

# Проверка Git
if ! command -v git &> /dev/null; then
    echo "[ERROR] Git не установлен!"
    echo "Установите Git: https://git-scm.com/"
    exit 1
fi

# Инициализация (если нужно)
if [ ! -d .git ]; then
    echo "[1/7] Инициализация Git..."
    git init
else
    echo "[1/7] Git уже инициализирован"
fi

# Добавление файлов
echo "[2/7] Добавление файлов..."
git add .

# Проверка статуса
echo "[3/7] Проверка файлов..."
git status --short

# Коммит
echo "[4/7] Создание коммита..."
git commit -m "Initial commit: Content Search System with Web Dashboard"

# Добавление remote
echo "[5/7] Подключение к GitHub..."
git remote remove origin 2>/dev/null
git remote add origin https://github.com/sergiiKols/smi.git

# Переименование ветки
echo "[6/7] Настройка ветки main..."
git branch -M main

# Push
echo "[7/7] Загрузка на GitHub..."
git push -u origin main

echo ""
echo "========================================"
echo "  ГОТОВО!"
echo "  https://github.com/sergiiKols/smi"
echo "========================================"