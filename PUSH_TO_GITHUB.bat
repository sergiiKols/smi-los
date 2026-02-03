@echo off
chcp 65001 >nul
echo ═══════════════════════════════════════════════════════════════
echo   ЗАГРУЗКА НА GITHUB
echo   Repository: sergiiKols/smi
echo ═══════════════════════════════════════════════════════════════
echo.
echo Проект подготовлен и готов к загрузке!
echo.
echo ⚠️  ВАЖНО: Git запросит учетные данные
echo.
echo Username: sergiiKols
echo Password: [ваш Personal Access Token]
echo.
echo 🔑 Как получить токен:
echo    1. https://github.com/settings/tokens
echo    2. Generate new token (classic)
echo    3. Выберите scope: repo
echo    4. Скопируйте токен
echo.
echo Нажмите любую клавишу для начала загрузки...
pause >nul
echo.
echo ═══════════════════════════════════════════════════════════════
echo Загрузка началась...
echo ═══════════════════════════════════════════════════════════════
echo.

git push -u origin main

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo   ✅ УСПЕШНО ЗАГРУЖЕНО!
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo 🔗 Проверьте: https://github.com/sergiiKols/smi
    echo.
    echo 🚀 Следующие шаги:
    echo    1. Откройте репозиторий на GitHub
    echo    2. Разверните на Vercel ^(см. DEPLOYMENT.md^)
    echo    3. Настройте API ключи
    echo.
) else (
    echo.
    echo ═══════════════════════════════════════════════════════════════
    echo   ⚠️  ОШИБКА ЗАГРУЗКИ
    echo ═══════════════════════════════════════════════════════════════
    echo.
    echo Возможные причины:
    echo    • Неправильные учетные данные
    echo    • Нет доступа к интернету
    echo    • Проблемы с GitHub
    echo.
    echo Попробуйте снова или используйте GitHub Desktop
    echo https://desktop.github.com/
    echo.
)

pause
