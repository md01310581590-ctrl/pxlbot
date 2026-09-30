from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import FOUNDER_USERNAME, CHANNEL_URL

def get_main_menu_kb() -> InlineKeyboardMarkup:
    founder_url = f"https://t.me/{FOUNDER_USERNAME}" if FOUNDER_USERNAME else "https://t.me/Nicky_pxl"
    channel_url = CHANNEL_URL or "https://t.me/pxlbot_studios"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🚀 Проекты и Кейсы", callback_data="cases_menu"),
                InlineKeyboardButton(text="📂 Услуги и Тарифы", callback_data="services_menu")
            ],
            [
                InlineKeyboardButton(text="🛡 Сопровождение и SLA", callback_data="support_menu")
            ],
            [
                InlineKeyboardButton(text="🧮 Рассчитать проект (за 1 мин)", callback_data="start_calc")
            ],
            [
                InlineKeyboardButton(text="📈 Инвесторам (Venture)", callback_data="venture_menu"),
                InlineKeyboardButton(text="📢 Наш канал", url=channel_url)
            ],
            [
                InlineKeyboardButton(text="💬 Написать основателю (@Nicky_pxl)", url=founder_url)
            ]
        ]
    )

def get_cases_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌾 Флагман: «Агротерминал» & «Агротрейд» (TMA)", callback_data="case_agro")],
            [InlineKeyboardButton(text="⚖️ Флагман: «ЮрБиржа» (LegalTech TMA & Escrow)", callback_data="case_legal")],
            [InlineKeyboardButton(text="🛍 Кейс: Интернет-магазин в Telegram (Mini App)", callback_data="case_miniapp")],
            [InlineKeyboardButton(text="🚗 Кейс: Автосервис & Детейлинг (Калькулятор)", callback_data="case_auto")],
            [InlineKeyboardButton(text="💈 Кейс: Сеть услуг & Клиника (Запись 24/7)", callback_data="case_beauty")],
            [InlineKeyboardButton(text="📋 Кейс: Квиз-воронка (Недвижимость / Ремонт)", callback_data="case_quiz")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_single_case_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🎯 Хочу похожее решение", callback_data="start_order")],
            [InlineKeyboardButton(text="🧮 Рассчитать под мою нишу", callback_data="start_calc")],
            [InlineKeyboardButton(text="📂 Все проекты и кейсы", callback_data="cases_menu")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_services_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🧮 Рассчитать стоимость моего проекта", callback_data="start_calc")],
            [InlineKeyboardButton(text="🛡 Подробнее про сопровождение и SLA", callback_data="support_menu")],
            [InlineKeyboardButton(text="📝 Оставить заявку на разработку", callback_data="start_order")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_support_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🚑 Починить / Взять на баланс моего бота", callback_data="start_support_audit")],
            [InlineKeyboardButton(text="🛡 Подключить сопровождение (SLA / Growth)", callback_data="start_order")],
            [InlineKeyboardButton(text="📂 Тарифы на разработку с нуля", callback_data="services_menu")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_venture_kb() -> InlineKeyboardMarkup:
    founder_url = f"https://t.me/{FOUNDER_USERNAME}" if FOUNDER_USERNAME else "https://t.me/Nicky_pxl"
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🌾 Подробнее: Агротерминал & Агротрейд", callback_data="case_agro")],
            [InlineKeyboardButton(text="⚖️ Подробнее: ЮрБиржа (Escrow TMA)", callback_data="case_legal")],
            [InlineKeyboardButton(text="💼 Запросить питч-дек и демо (@Nicky_pxl)", url=founder_url)],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

# Клавиатуры для калькулятора
def get_calc_product_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📋 Квиз-воронка / Лид-бот (25–40 тыс. ₽)", callback_data="calc_prod_quizbot")],
            [InlineKeyboardButton(text="🤖 Бизнес-бот с CRM / Оплатой / AI (50–85 тыс. ₽)", callback_data="calc_prod_bizbot")],
            [InlineKeyboardButton(text="📱 Telegram Mini App / WebApp (95–190 тыс. ₽)", callback_data="calc_prod_miniapp")],
            [InlineKeyboardButton(text="🚑 Доработка / Реанимация готового бота", callback_data="calc_prod_reanimate")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="to_main_menu")]
        ]
    )

def get_calc_niche_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📦 E-commerce / Селлеры / Торговля", callback_data="calc_niche_ecom")],
            [InlineKeyboardButton(text="🏗 Недвижимость / Строительство / Ремонт", callback_data="calc_niche_repair")],
            [InlineKeyboardButton(text="🚗 Автобизнес / Сервис / Логистика", callback_data="calc_niche_auto")],
            [InlineKeyboardButton(text="🏥 Клиники / Услуги / EdTech", callback_data="calc_niche_beauty")],
            [InlineKeyboardButton(text="🏢 B2B-сервис / Стартап / Другая ниша", callback_data="calc_niche_other")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="to_main_menu")]
        ]
    )

def get_calc_integration_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📊 Выгрузка в CRM (AmoCRM / Bitrix24 / Таблицы)", callback_data="calc_int_crm")],
            [InlineKeyboardButton(text="💳 Прием оплат (СБП / ЮKassa / Эквайринг)", callback_data="calc_int_pay")],
            [InlineKeyboardButton(text="⚡️ Полный контур (CRM + Оплата + AI / Админка)", callback_data="calc_int_all")],
            [InlineKeyboardButton(text="🚫 Базовый контур (уведомления внутри Telegram)", callback_data="calc_int_none")],
            [InlineKeyboardButton(text="❌ Отмена", callback_data="to_main_menu")]
        ]
    )

def get_calc_result_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="📨 Зафиксировать расчет и получить КП", callback_data="calc_submit_order")],
            [InlineKeyboardButton(text="🔄 Пересчитать параметры", callback_data="start_calc")],
            [InlineKeyboardButton(text="🔙 Главное меню", callback_data="to_main_menu")]
        ]
    )

def get_cancel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="❌ Отмена", callback_data="to_main_menu")]
        ]
    )
