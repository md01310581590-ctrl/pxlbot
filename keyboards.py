from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FOUNDER_USERNAME, CHANNEL_URL

def get_founder_url() -> str:
    return f"https://t.me/{FOUNDER_USERNAME}" if FOUNDER_USERNAME else "https://t.me/Nicky_pxl"

def get_channel_url() -> str:
    return CHANNEL_URL or "https://t.me/pxlbot_studios"

def get_main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🧮 Рассчитать проект за 1 минуту", callback_data="start_calc")
            ],
            [
                InlineKeyboardButton(text="🚀 Кейсы и окупаемость", callback_data="cases_menu"),
                InlineKeyboardButton(text="📂 Тарифы и пакеты под ключ", callback_data="services_menu")
            ],
            [
                InlineKeyboardButton(text="💬 Написать основателю (@Nicky_pxl)", url=get_founder_url())
            ],
            [
                InlineKeyboardButton(text="📢 Наш канал", url=get_channel_url()),
                InlineKeyboardButton(text="💼 О студии / Venture", callback_data="venture_menu")
            ]
        ]
    )

def get_cases_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌾 B2B-терминал: «Агротерминал» (TradingView & Netback)", callback_data="case_agro")],
            [InlineKeyboardButton(text="⚖️ LegalTech: «ЮрБиржа» (Escrow & Проверка юристов)", callback_data="case_legal")],
            [InlineKeyboardButton(text="🛍 E-commerce: Онлайн-магазин в Telegram (Mini App)", callback_data="case_miniapp")],
            [InlineKeyboardButton(text="🚗 Автобизнес: Интерактивный калькулятор ТО и заезда", callback_data="case_auto")],
            [InlineKeyboardButton(text="💈 Сфера услуг: Запись 24/7 и борьба с неявками", callback_data="case_beauty")],
            [InlineKeyboardButton(text="📋 Квиз-воронка: Лидген в недвижимости и ремонте", callback_data="case_quiz")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_single_case_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎯 Хочу похожее решение для бизнеса", callback_data="start_order")],
            [InlineKeyboardButton(text="🧮 Рассчитать под мою сферу", callback_data="start_calc")],
            [InlineKeyboardButton(text="📂 Все проекты и кейсы", callback_data="cases_menu")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_services_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎁 Комплекты «Всё включено» (Выгода до 30%)", callback_data="bundles_menu")],
            [InlineKeyboardButton(text="⚙️ Базовая разработка по модулям", callback_data="modules_menu")],
            [InlineKeyboardButton(text="🛡 Техподдержка и сервер", callback_data="support_menu")],
            [InlineKeyboardButton(text="🧮 Рассчитать точную смету проекта", callback_data="start_calc")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_modules_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧮 Рассчитать в калькуляторе", callback_data="start_calc")],
            [InlineKeyboardButton(text="🎁 Комплекты «Всё включено»", callback_data="bundles_menu")],
            [InlineKeyboardButton(text="📝 Обсудить проект с инженером", callback_data="start_order")],
            [InlineKeyboardButton(text="🔙 Все тарифы и пакеты", callback_data="services_menu")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

# Клавиатуры для комплексных пакетов (Bundles)
def get_bundles_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="⚡️ «Быстрый старт 360°» (39 900 ₽)", callback_data="bundle_start")],
            [InlineKeyboardButton(text="🚀 «Турбо-продажи + Маркетинг» (89 000 ₽)", callback_data="bundle_sales")],
            [InlineKeyboardButton(text="💎 «Digital-Экосистема PRO» (199 000 ₽)", callback_data="bundle_pro")],
            [InlineKeyboardButton(text="🧮 Рассчитать индивидуальный проект", callback_data="start_calc")],
            [InlineKeyboardButton(text="📂 Все тарифы и пакеты", callback_data="services_menu")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_single_bundle_kb(bundle_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎯 Забронировать этот комплект под ключ", callback_data=f"order_bundle_{bundle_code}")],
            [InlineKeyboardButton(text="💬 Обсудить детали с инженером", url=get_founder_url())],
            [InlineKeyboardButton(text="📦 Все комплексные пакеты", callback_data="bundles_menu")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_support_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Мой статус техподдержки и гарантии", callback_data="support_status")],
            [InlineKeyboardButton(text="🛡 Тариф «Базовый» (5 900 ₽/мес)", callback_data="support_plan_base")],
            [InlineKeyboardButton(text="🚀 Тариф «Развитие + Рассылка» (12 900 ₽/мес)", callback_data="support_plan_growth")],
            [InlineKeyboardButton(text="💎 Тариф «Выделенный IT-отдел» (24 900 ₽/мес)", callback_data="support_plan_pro")],
            [InlineKeyboardButton(text="🚑 Перенести / Реанимировать чужого бота", callback_data="start_support_audit")],
            [InlineKeyboardButton(text="📂 Все тарифы и пакеты", callback_data="services_menu")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_support_plan_detail_kb(plan_code: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Выбрать этот тариф техподдержки", callback_data=f"select_plan_{plan_code}")],
            [InlineKeyboardButton(text="📊 Проверить мой статус и дни", callback_data="support_status")],
            [InlineKeyboardButton(text="💬 Задать вопрос инженеру (@Nicky_pxl)", url=get_founder_url())],
            [InlineKeyboardButton(text="🔙 Все тарифы техподдержки", callback_data="support_menu")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_support_status_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔄 Сменить тариф техподдержки", callback_data="support_menu")],
            [InlineKeyboardButton(text="💬 Написать ведущему инженеру", url=get_founder_url())],
            [InlineKeyboardButton(text="🎁 Выбрать комплект «Всё включено»", callback_data="bundles_menu")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_venture_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌾 Подробнее: Агротерминал & Агротрейд", callback_data="case_agro")],
            [InlineKeyboardButton(text="⚖️ Подробнее: ЮрБиржа (Escrow TMA)", callback_data="case_legal")],
            [InlineKeyboardButton(text="💼 Запросить питч-дек и демо (@Nicky_pxl)", url=get_founder_url())],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

# ────────────────────────── ТОЧНЫЙ 4-ШАГОВЫЙ КАЛЬКУЛЯТОР ──────────────────────────

def get_calc_product_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Квиз-воронка / Лид-бот (25 000 ₽)", callback_data="calc_prod_quizbot")],
            [InlineKeyboardButton(text="🛍 Каталог товаров/услуг с корзиной (38 000 ₽)", callback_data="calc_prod_catalog")],
            [InlineKeyboardButton(text="💈 Бот онлайн-записи и бронирования (35 000 ₽)", callback_data="calc_prod_booking")],
            [InlineKeyboardButton(text="📱 Telegram Mini App / WebApp (85 000 ₽)", callback_data="calc_prod_miniapp")],
            [InlineKeyboardButton(text="🚑 Реанимация / Доработка чужого бота (15 000 ₽)", callback_data="calc_prod_reanimate")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="to_main_menu")]
        ]
    )

def get_calc_niche_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 E-commerce / Селлеры / Торговля", callback_data="calc_niche_ecom")],
            [InlineKeyboardButton(text="🚗 Автобизнес / Сервис / Логистика", callback_data="calc_niche_auto")],
            [InlineKeyboardButton(text="💈 Клиники / Салоны / Сфера услуг", callback_data="calc_niche_beauty")],
            [InlineKeyboardButton(text="🏗 Недвижимость / Ремонт / Производство", callback_data="calc_niche_repair")],
            [InlineKeyboardButton(text="🏢 B2B-услуги / Опт / Образование", callback_data="calc_niche_other")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="to_main_menu")]
        ]
    )

def get_calc_integration_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚫 Базовый контур (уведомления в Telegram) (+0 ₽)", callback_data="calc_int_none")],
            [InlineKeyboardButton(text="📊 Интеграция с CRM (AmoCRM / Bitrix24) (+10 000 ₽)", callback_data="calc_int_crm")],
            [InlineKeyboardButton(text="💳 Прием оплат (СБП, ЮKassa, карты) (+10 000 ₽)", callback_data="calc_int_pay")],
            [InlineKeyboardButton(text="⚡️ Полный контур (CRM + Оплата + чеки) (+18 000 ₽)", callback_data="calc_int_all")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="to_main_menu")]
        ]
    )

def get_calc_addon_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="💬 AI-консультант (ChatGPT / Умные ответы 24/7) (+12 000 ₽)", callback_data="calc_add_ai")],
            [InlineKeyboardButton(text="📢 Модуль авторассылок и сбора базы (+7 000 ₽)", callback_data="calc_add_broadcast")],
            [InlineKeyboardButton(text="🎁 Включить 3 мес. техподдержки и рассылок (+19 000 ₽)", callback_data="calc_add_support3m")],
            [InlineKeyboardButton(text="⏩ Без доп. модулей (базовый запуск) (+0 ₽)", callback_data="calc_add_none")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="to_main_menu")]
        ]
    )

def get_calc_result_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📨 Зафиксировать смету и получить КП", callback_data="calc_submit_order")],
            [InlineKeyboardButton(text="🔄 Пересчитать параметры", callback_data="start_calc")],
            [InlineKeyboardButton(text="🎁 Посмотреть комплекты «Всё включено»", callback_data="bundles_menu")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="to_main_menu")]
        ]
    )
