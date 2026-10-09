@echo off
chcp 65001 > nul
title PxlBot Studios Bot Runner

echo ======================================================
echo   👾 PXLBOT STUDIOS // ЗАПУСК СТУДИЙНОГО БОТА
echo ======================================================
echo.

echo [1/2] Проверка и установка библиотек...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo Ошибка при установке библиотек. Убедитесь, что Python установлен и добавлен в PATH.
    pause
    exit /b
)

echo.
echo [2/2] Запуск бота...
echo.
python main.py

pause
