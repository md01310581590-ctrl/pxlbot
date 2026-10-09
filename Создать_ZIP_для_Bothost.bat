@echo off
chcp 65001 >nul
cd /d "%~dp0"
python -c "import zipfile, os; files=['main.py','config.py','handlers.py','keyboards.py','states.py','smeta_generator.py','requirements.txt','Dockerfile','.env']; files=[f for f in files if os.path.exists(f)]; files += ['media_cache.json'] if os.path.exists('media_cache.json') else []; z=zipfile.ZipFile(r'..\pxlbot_bothost_deploy.zip','w',zipfile.ZIP_DEFLATED); [z.write(f,f) for f in files]; z.close(); print('OK')"
echo ===============================================================
echo Готовый архив pxlbot_bothost_deploy.zip создан на Рабочем столе!
echo Его можно загрузить в панель Bothost.ru
echo ===============================================================
pause
