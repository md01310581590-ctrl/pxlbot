import os
from dotenv import load_dotenv

load_dotenv()

# Читаем токен из переменной окружения (BOT_TOKEN или TOKEN, которые передает Bothost / .env)
BOT_TOKEN = (
    os.getenv("BOT_TOKEN")
    or os.getenv("TOKEN")
    or os.getenv("TELEGRAM_BOT_TOKEN")
    or ""
).strip()

ADMIN_ID_RAW = os.getenv("ADMIN_ID", "0").strip()
FOUNDER_USERNAME = os.getenv("FOUNDER_USERNAME", "Nicky_pxl").strip().replace("@", "")
CHANNEL_URL = os.getenv("CHANNEL_URL", "https://t.me/pxlbot_studios").strip()

try:
    ADMIN_ID = int(ADMIN_ID_RAW)
except ValueError:
    ADMIN_ID = 0
