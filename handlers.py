from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards import (
    get_main_menu_kb,
    get_showroom_kb,
    get_legal_case_kb,
    get_auto_case_kb,
    get_agro_case_kb,
    get_single_case_kb,
    get_services_kb,
    get_modules_kb,
    get_bundles_menu_kb,
    get_single_bundle_kb,
    get_support_menu_kb,
    get_support_plan_detail_kb,
    get_support_status_kb,
    get_about_kb,
    get_venture_kb,
    get_calc_product_kb,
    get_calc_niche_kb,
    get_calc_integration_kb,
    get_calc_addon_kb,
    get_calc_result_kb,
    get_cancel_kb,
    get_founder_url,
    get_channel_url
)
from states import CalculatorStates, OrderStates, SupportAuditStates, BundleOrderStates
from config import ADMIN_ID, FOUNDER_USERNAME
import os
try:
    from smeta_generator import generate_smeta_docx
except Exception as _e:
    generate_smeta_docx = None

router = Router()

DYNAMIC_ADMIN_FILE = "admin_id.txt"
USER_PLANS_FILE = "user_plans.json"
MEDIA_CACHE_FILE = "media_cache.json"
DIVIDER = "――――――――――\n"

# ────────────────────────── ХРАНЕНИЕ ДАННЫХ И СТАТУСОВ ──────────────────────────

def get_admin_id() -> int:
    if ADMIN_ID and ADMIN_ID != 0:
        return ADMIN_ID
    if os.path.exists(DYNAMIC_ADMIN_FILE):
        try:
            with open(DYNAMIC_ADMIN_FILE, "r", encoding="utf-8") as f:
                return int(f.read().strip())
        except Exception:
            pass
    return 0

def save_admin_id_if_founder(user) -> None:
    if not user:
        return
    uname = (user.username or "").lower()
    if uname == (FOUNDER_USERNAME or "nicky_pxl").lower():
        try:
            with open(DYNAMIC_ADMIN_FILE, "w", encoding="utf-8") as f:
                f.write(str(user.id))
        except Exception:
            pass

def get_cached_media(key: str) -> str:
    if os.path.exists(MEDIA_CACHE_FILE):
        try:
            with open(MEDIA_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get(key, "")
        except Exception:
            pass
    return ""

def set_cached_media(key: str, val: str) -> None:
    data = {}
    if os.path.exists(MEDIA_CACHE_FILE):
        try:
            with open(MEDIA_CACHE_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            pass
    data[key] = val
    try:
        with open(MEDIA_CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

async def safe_send_or_edit(call: CallbackQuery, text: str, reply_markup=None, parse_mode="HTML", disable_web_page_preview=True):
    try:
        await call.message.edit_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )
    except Exception:
        try:
            await call.message.delete()
        except Exception:
            pass
        await call.message.answer(
            text=text,
            reply_markup=reply_markup,
            parse_mode=parse_mode,
            disable_web_page_preview=disable_web_page_preview
        )

def get_legal_video():
    file_id = get_cached_media("legal_video_file_id")
    if file_id:
        return file_id, "file_id"
    candidates = [
        os.path.join(os.path.dirname(__file__), "media", "legal_demo.mp4"),
        os.path.join(os.path.dirname(__file__), "media", "итог 1.mp4"),
        os.path.expanduser(r"~\Desktop\итог 1.mp4"),
        r"C:\Users\Валера куплю гараж\Desktop\итог 1.mp4"
    ]
    for p in candidates:
        if os.path.exists(p):
            sz = os.path.getsize(p)
            if sz <= 49 * 1024 * 1024:
                return FSInputFile(p), "local_file"
            else:
                return p, "too_large"
    return None, None

PLANS_CATALOG = {
    "base": {
        "title": "Тариф «Базовый» (Сервер + Контроль 24/7) — 5 900 ₽/мес",
        "name": "«Базовый» (Сервер + Защита)",
        "price": "5 900 ₽/мес",
        "reaction": "до 4 часов",
        "hours": "до 2 часов работы инженера в месяц",
        "description": "Размещение на защищенном VPS-сервере в РФ (152-ФЗ), мониторинг доступности 24/7, ежедневные бэкапы базы данных, правки цен, текстов, фото и кнопок по вашей заявке."
    },
    "growth": {
        "title": "Тариф «Развитие + Рассылка» — 12 900 ₽/мес (Хит продаж)",
        "name": "«Развитие + Рассылка» (Хит продаж)",
        "price": "12 900 ₽/мес",
        "reaction": "приоритетная до 1 часа 24/7",
        "hours": "до 5 часов работы инженера в месяц",
        "description": "Предоставление сервера в РФ, доработка сценариев и интеграций по вашей заявке + подготовка и отправка 1 промо-рассылки в месяц по вашей базе клиентов с маркировкой ОРД/erid по закону."
    },
    "pro": {
        "title": "Тариф «Выделенный IT-отдел» — 24 900 ₽/мес",
        "name": "«Выделенный IT-отдел» (Под ключ)",
        "price": "24 900 ₽/мес",
        "reaction": "экстренная до 30 минут 24/7",
        "hours": "до 10 часов разработки в месяц",
        "description": "Выделенный мощный сервер под высокую нагрузку, экстренная помощь до 30 мин, внедрение новых экранов и фич по ТЗ клиента, до 3 рассылок в месяц и юридическое сопровождение."
    }
}

BUNDLES_CATALOG = {
    "start": {
        "title": "⚡️ Комплект «Быстрый старт 360°»",
        "price": "39 900 ₽",
        "old_price": "55 000 ₽",
        "economy": "15 100 ₽",
        "term": "3–5 рабочих дней",
        "support": "3 месяца техподдержки (включая сервер в РФ)",
        "desc": (
            "Идеально для сферы услуг, автобизнеса, медицины, ремонта и B2B.\n\n"
            "<b>Что входит в комплект («Всё включено»):</b>\n"
            "✅ <b>Разработка под ключ:</b> квиз-воронка / лид-бот с расчетом цены и квалификацией за 30 сек;\n"
            "✅ <b>Интеграция:</b> моментальная выгрузка заявок в рабочий Telegram-чат компании или Google Таблицы;\n"
            "✅ <b>Техподдержка (3 месяца):</b> предоставление защищенного VPS-сервера в РФ, ежедневные бэкапы, мониторинг 24/7 и мелкие правки инженером по вашей заявке;\n"
            "✅ <b>Юридический контур:</b> пакет документов и согласие по 152-ФЗ.\n\n"
            "💡 <i>Один фиксированный платеж — и на 3 месяца вы полностью закрываете вопросы с разработкой, хостингом и поддержкой.</i>"
        )
    },
    "sales": {
        "title": "🚀 Комплект «Турбо-продажи + Маркетинг»",
        "price": "89 000 ₽",
        "old_price": "125 000 ₽",
        "economy": "36 000 ₽",
        "term": "7–14 рабочих дней",
        "support": "3 месяца техподдержки (включая сервер в РФ) + 3 рассылки",
        "desc": (
            "Хит продаж для торговли, интернет-магазинов, селлеров, оптовиков и онлайн-школ.\n\n"
            "<b>Что входит в комплект («Всё включено»):</b>\n"
            "✅ <b>Разработка под ключ:</b> автономный отдел продаж (витрина товаров/услуг, фильтры, корзина, онлайн-оплата СБП/ЮKassa и чеки 54-ФЗ);\n"
            "✅ <b>Интеграция:</b> двухсторонняя синхронизация с AmoCRM / Bitrix24 и МойСклад + админ-панель;\n"
            "✅ <b>Техподдержка (3 месяца):</b> предоставление сервера в РФ, приоритетная реакция инженера (до 1ч 24/7) и до 5ч правок в месяц по вашей заявке;\n"
            "✅ <b>Рассылки (3 месяца):</b> подготовка и запуск 3 промо-рассылок по вашей базе клиентов (по 1 в месяц) с маркировкой рекламы ОРД/erid по закону.\n\n"
            "📈 <i>Готовая система продаж: бот принимает оплаты, передает заказы в CRM и делает регулярные повторные продажи по базе.</i>"
        )
    },
    "pro": {
        "title": "💎 Комплект «Digital-Экосистема Mini App PRO»",
        "price": "199 000 ₽",
        "old_price": "310 000 ₽",
        "economy": "111 000 ₽",
        "term": "3–4 недели",
        "support": "6 месяцев техподдержки с выделенным сервером",
        "desc": (
            "Флагманское решение для стартапов, сетей, маркетплейсов и сервисов с личным кабинетом.\n\n"
            "<b>Что входит в комплект («Всё включено»):</b>\n"
            "✅ <b>Разработка под ключ:</b> кастомный Telegram Mini App (React + Python Backend) с интерфейсом мобильного приложения прямо в чате;\n"
            "✅ <b>Архитектура:</b> личные кабинеты, сложные расчеты, безопасные сделки (Escrow), партнерская программа;\n"
            "✅ <b>Техподдержка (6 месяцев):</b> выделенный мощный сервер под нагрузку (Stage+Prod), реакция до 30 мин 24/7;\n"
            "✅ <b>До 10 часов доработок ежемесячно (до 60 часов за полгода):</b> внедрение новых экранов и фич по ТЗ клиента;\n"
            "✅ <b>Рассылки и Legal:</b> до 3 рассылок в месяц по базе клиентов с маркировкой ОРД/erid и юридический щит."
        )
    }
}

# ────────────────────────── СПРАВОЧНИКИ ТОЧНОГО КАЛЬКУЛЯТОРА ──────────────────────────

CALC_PRODUCTS = {
    "quizbot": {"title": "Квиз-воронка / Лид-бот", "price": 25000, "days": 4},
    "catalog": {"title": "Каталог товаров/услуг с корзиной", "price": 38000, "days": 8},
    "booking": {"title": "Бот онлайн-записи и бронирования", "price": 35000, "days": 6},
    "miniapp": {"title": "Telegram Mini App (WebApp)", "price": 85000, "days": 18},
    "reanimate": {"title": "Реанимация / Доработка чужого бота", "price": 15000, "days": 2}
}

CALC_NICHES = {
    "ecom": "E-commerce / Торговля / Селлеры",
    "auto": "Автобизнес / Сервис / Логистика",
    "beauty": "Клиники / Салоны / Сфера услуг",
    "repair": "Недвижимость / Ремонт / Производство",
    "other": "B2B-услуги / Опт / Образование"
}

CALC_INTEGRATIONS = {
    "none": {"title": "Базовый контур (уведомления в Telegram)", "price": 0, "days": 0},
    "crm": {"title": "Интеграция с CRM (AmoCRM / Bitrix24)", "price": 10000, "days": 2},
    "pay": {"title": "Прием онлайн-оплат (СБП, ЮKassa, карты)", "price": 10000, "days": 2},
    "all": {"title": "Полный контур (CRM + Оплата + чеки)", "price": 18000, "days": 3}
}

CALC_ADDONS = {
    "none": {"title": "Без доп. модулей (базовый запуск)", "price": 0, "days": 0},
    "ai": {"title": "AI-консультант (ChatGPT / Умные ответы 24/7)", "price": 12000, "days": 2},
    "broadcast": {"title": "Модуль авторассылок и сбора базы", "price": 7000, "days": 1},
    "support3m": {"title": "3 мес. техподдержки и рассылок под ключ", "price": 19000, "days": 0}
}

def load_user_plans() -> dict:
    if os.path.exists(USER_PLANS_FILE):
        try:
            with open(USER_PLANS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def save_user_plans(data: dict) -> None:
    try:
        with open(USER_PLANS_FILE, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except Exception:
        pass

def get_user_plan_info(user_id: int) -> dict:
    plans = load_user_plans()
    uid = str(user_id)
    if uid in plans:
        return plans[uid]
    return {
        "plan_key": "growth",
        "plan_title": PLANS_CATALOG["growth"]["title"],
        "warranty_days": 15,
        "starts_at": "С момента сдачи готового бота в эксплуатацию",
        "status": "Гарантийный период 15 дней включен",
        "channel": "@Nicky_pxl (ведущий инженер)"
    }

def set_user_plan(user_id: int, plan_key: str) -> None:
    plans = load_user_plans()
    uid = str(user_id)
    plan_data = PLANS_CATALOG.get(plan_key, PLANS_CATALOG["growth"])
    plans[uid] = {
        "plan_key": plan_key,
        "plan_title": plan_data["title"],
        "warranty_days": 15,
        "starts_at": "С момента сдачи готового бота в эксплуатацию",
        "status": "Гарантийный период 15 дней включен",
        "channel": "@Nicky_pxl (ведущий инженер)"
    }
    save_user_plans(plans)

# ────────────────────────── ГЛАВНОЕ МЕНЮ ──────────────────────────

MAIN_WELCOME_TEXT = (
    "👾 <b>PXLBOT STUDIOS // АВТОМАТИЗАЦИЯ И ПРОДАЖИ В TELEGRAM</b>\n"
    + DIVIDER +
    "Помогаем бизнесу перестать сливать клиентов из-за долгих ответов, "
    "забирать заявки за 30 секунд 24/7 (даже ночью и в выходные) и автоматизировать рутину менеджеров.\n\n"
    "<b>Что вы получаете, работая с нами:</b>\n"
    "• <b>Захват лида за 30 секунд 24/7</b> — расчет сметы и квалификация без задержек\n"
    "• <b>Автономные продажи</b> — каталог, онлайн-оплата (СБП/карты) и выгрузка в CRM\n"
    "• <b>Чистый кастомный код</b> — никаких конструкторов и абонентской платы платформам\n"
    "• <b>Юридическая защита</b> — соответствие 152-ФЗ и маркировка рекламы (ОРД/erid)\n"
    "• <b>15 дней сервера и техподдержки в подарок*</b>\n\n"
    "<i>*При подключении любого тарифа техподдержки: первые 15 дней бесплатны со дня сдачи готового бота в работу. "
    "Вы тестируете бота на реальном трафике без риска, а первый счет выставляется только на 16-й день.</i>\n\n"
    "👇 Выберите нужное действие ниже:"
)

@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    save_admin_id_if_founder(message.from_user)
    await message.answer(
        text=MAIN_WELCOME_TEXT,
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "to_main_menu")
async def cb_main_menu(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await safe_send_or_edit(
        call,
        text=MAIN_WELCOME_TEXT,
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )
    await call.answer()

# ────────────────────────── ШОУРУМ РЕШЕНИЙ (ДЕМО-СТЕНДЫ) ──────────────────────────

@router.callback_query(F.data == "showroom_menu")
async def cb_showroom_menu(call: CallbackQuery):
    text = (
        "🎪 <b>ШОУРУМ РЕШЕНИЙ PXLBOT STUDIOS // ДЕМО-СТЕНДЫ</b>\n"
        + DIVIDER +
        "Здесь собраны интерактивные демонстрации наших продуктов. "
        "Вы можете протестировать живые решения и оценить скорость и UX:\n\n"
        "🚗 <b>1. Автобизнес & Детейлинг (@apex_detail_demo_bot):</b>\n"
        "Интерактивный калькулятор ТО и услуг за 20 секунд с бронированием.\n"
        "👉 <a href=\"https://t.me/pxlbot_studios/30\">Ссылка на пост о шоуруме в канале</a>\n\n"
        "⚖️ <b>2. LegalTech «ЮрБиржа» (Escrow & TMA):</b>\n"
        "Полноценный маркетплейс услуг с безопасной сделкой и видео-демонстрацией.\n"
        "👉 <a href=\"https://t.me/pxlbot_studios/20\">Ссылка на пост о ЮрБирже в канале</a>\n\n"
        "🌾 <b>3. AgroTech «Агротерминал» (B2B):</b>\n"
        "Биржевой стакан и Netback калькулятор (в процессе пересборки и кастдевов).\n"
        "👉 <a href=\"https://t.me/pxlbot_studios/19\">Ссылка на пост об Агротерминале в канале</a>\n\n"
        "🛍 <b>4. E-commerce D2C Mini App:</b>\n"
        "Онлайн-магазин внутри Telegram с корзиной и оплатой в 1 клик.\n\n"
        "<i>Выберите интересующий демо-стенд ниже:</i>"
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_showroom_kb(), parse_mode="HTML", disable_web_page_preview=False)
    await call.answer()

@router.callback_query(F.data == "show_demo_auto")
async def cb_show_demo_auto(call: CallbackQuery):
    text = (
        "🚗 <b>ДЕМО-СТЕНД: ДЕТЕЙЛИНГ & АВТОСЕРВИС</b>\n"
        + DIVIDER +
        "Мы запустили полноценный тестовый бот-калькулятор для автобизнеса.\n\n"
        "<b>В демо-боте реализовано:</b>\n"
        "• Выбор класса автомобиля (седан, кроссовер, внедорожник);\n"
        "• Мгновенный расчет стоимости полировки, керамики, химчистки и ТО;\n"
        "• Выбор удобного времени и оформление записи на заезд;\n"
        "• Моментальная передача заявки мастеру-приемщику в CRM.\n\n"
        "🚀 <b>Попробуйте прямо сейчас:</b> @apex_detail_demo_bot\n"
        "👉 <b><a href=\"https://t.me/pxlbot_studios/30\">Ссылка на пост о шоуруме и автобизнесе в канале</a></b>"
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_auto_case_kb(), parse_mode="HTML", disable_web_page_preview=False)
    await call.answer()

# ────────────────────────── РАЗДЕЛ ШОУРУМА И РЕШЕНИЙ ──────────────────────────

@router.callback_query(F.data == "cases_menu")
async def cb_cases_menu(call: CallbackQuery):
    await cb_showroom_menu(call)

@router.callback_query(F.data == "case_agro")
async def cb_case_agro(call: CallbackQuery):
    text = (
        "🌾 <b>ФЛАГМАН: «Агротерминал» & «Агротрейд» (AgroTech B2B)</b>\n"
        + DIVIDER +
        "<b>Формат:</b> B2B-платформа и котировочный терминал (Telegram Mini App + Web)\n\n"
        "<b>Бизнес-задача:</b>\n"
        "Убрать хаос бесконечных чатов и посредников между производителями и экспортерами зерна.\n\n"
        "<b>Что реализовано в базовой версии:</b>\n"
        "• Графики цен TradingView по портам Новороссийска, Тамани и Ростова в реальном времени;\n"
        "• Калькулятор Netback («EXW Ангар»): моментальный расчет чистой цены тонны с вычетом ж/д, авто и рефакций за качество;\n"
        "• Биржевой стакан (Order Book) прямых закупок от экспортеров с фиксацией объема в 1 клик.\n\n"
        "🔄 <b>СТАТУС ПРОЕКТА: Глубокая пересборка и исследования рынка</b>\n"
        "<i>Сейчас мы проводим масштабные качественные кастдевы зерновых трейдеров и экспортеров, "
        "полностью пересобираем продуктовую логику и обновляем интерфейс терминала. "
        "Полноценная видео-демонстрация новой версии будет опубликована в ближайшее время!</i>\n\n"
        "👉 <b><a href=\"https://t.me/pxlbot_studios/19\">Ссылка на пост об Агротерминале в канале</a></b>\n\n"
        "💡 <i>Хотите подобный B2B-калькулятор или торговую площадку для своей ниши?</i>"
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_agro_case_kb(), parse_mode="HTML", disable_web_page_preview=False)
    await call.answer()

@router.callback_query(F.data == "case_legal")
async def cb_case_legal(call: CallbackQuery):
    text = (
        "⚖️ <b>ФЛАГМАН: «ЮрБиржа» (LegalTech Marketplace & Escrow)</b>\n"
        + DIVIDER +
        "<b>Формат:</b> Двухсторонний маркетплейс услуг внутри Telegram (Mini App)\n\n"
        "<b>Бизнес-задача:</b>\n"
        "Обеспечить безопасные сделки между заказчиками и юристами с гарантией выплаты.\n\n"
        "<b>Что реализовано:</b>\n"
        "• <b>Безопасная сделка (Escrow):</b> заморозка средств и выплата только после подтверждения результата;\n"
        "• <b>Проверка юристов:</b> верификация через госреестры (ФИС ФРДО и Минюст РФ);\n"
        "• <b>Интерактивный квиз-брифинг:</b> авто-распределение заявок проверенным экспертам.\n\n"
        "👉 <b><a href=\"https://t.me/pxlbot_studios/20\">Ссылка на подробный разбор решения в канале</a></b>\n\n"
        "💡 <i>Разрабатываем сервисы услуг, закрытые клубы и биржи с монетизацией под ключ.</i>"
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_legal_case_kb(), parse_mode="HTML", disable_web_page_preview=False)
    await call.answer()

@router.callback_query(F.data == "case_auto")
async def cb_case_auto(call: CallbackQuery):
    text = (
        "🚗 <b>КЕЙС & ШОУРУМ: Автосервис и детейлинг-центр</b>\n"
        + DIVIDER +
        "<b>Формат:</b> Интерактивный бот-калькулятор ТО и заезда с онлайн-бронированием\n\n"
        "<b>Проблема клиента:</b>\n"
        "Мастера тратили по 3 часа в день на ответы «Сколько стоит ТО на мою машину?», "
        "а клиенты уходили к конкурентам, пока ждали ответа.\n\n"
        "<b>Решение:</b>\n"
        "• Интерактивный бот с расчетом цены под марку авто и объем работ за 20 секунд;\n"
        "• Моментальный расчет сметы и онлайн-бронирование свободного бокса 24/7;\n"
        "• Готовая карточка клиента сразу уходит в CRM с телефоном и моделью авто.\n\n"
        "📈 <b>Результат:</b>\n"
        "• Ответ клиенту сократился с 15 минут до <b>20 секунд</b>;\n"
        "• Записи на сервис выросли на <b>+42%</b> без увеличения бюджета на рекламу.\n\n"
        "👉 <b><a href=\"https://t.me/pxlbot_studios/30\">Ссылка на пост о шоуруме и детейлинге в канале</a></b>\n"
        "🚀 <b><a href=\"https://t.me/apex_detail_demo_bot\">Открыть живой демо-стенд калькулятора</a></b>"
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_auto_case_kb(), parse_mode="HTML", disable_web_page_preview=False)
    await call.answer()

@router.callback_query(F.data == "case_miniapp")
async def cb_case_miniapp(call: CallbackQuery):
    text = (
        "🛍 <b>КЕЙС: Онлайн-магазин в Telegram (Mini App)</b>\n"
        + DIVIDER +
        "<b>Проблема клиента:</b>\n"
        "Сайт долго грузился на смартфонах, до 60% посетителей уходили без покупки, "
        "а разработка приложения в AppStore стоила от 700 000 ₽.\n\n"
        "<b>Решение:</b>\n"
        "• Запуск Mini App прямо в чате: открывается мгновенно, без скачивания;\n"
        "• Каталог, фильтры, корзина и оплата в 1 клик через СБП / ЮKassa;\n"
        "• Авто-отправка заказа в CRM и на склад (МойСклад);\n"
        "• 100% соблюдение 152-ФЗ (согласие и оферта).\n\n"
        "📈 <b>Результат:</b>\n"
        "• Конверсия в оплату выросла в <b>2.4 раза</b>;\n"
        "• Запуск состоялся в 5 раз дешевле классического мобильного приложения."
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_single_case_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "case_beauty")
async def cb_case_beauty(call: CallbackQuery):
    text = (
        "💈 <b>КЕЙС: Сеть клиник и салонов красоты</b>\n"
        + DIVIDER +
        "<b>Проблема клиента:</b>\n"
        "Заявки с рекламы поступали неравномерно, многие остывали до ответа менеджера. "
        "Высокий процент забытых визитов (до 30% клиентов не приходили).\n\n"
        "<b>Решение:</b>\n"
        "• Круглосуточная запись в 4 клика с выбором мастера и филиала;\n"
        "• Автоматическая цепочка напоминаний за 24 часа и за 2 часа до визита;\n"
        "• Автоматический сбор отзывов и реактивация спящей базы через рассылки.\n\n"
        "📈 <b>Результат:</b>\n"
        "• <b>+28% подтвержденных записей</b> на том же трафике;\n"
        "• Доля неявок (No-Show) снизилась на <b>65%</b>."
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_single_case_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "case_quiz")
async def cb_case_quiz(call: CallbackQuery):
    text = (
        "📋 <b>КЕЙС: Недвижимость и дизайн интерьеров</b>\n"
        + DIVIDER +
        "<b>Проблема клиента:</b>\n"
        "Сайт приносил дорогие лиды по 2 300 ₽, при этом менеджеры тратили время "
        "на обзвон людей, которые просто случайно оставили номер.\n\n"
        "<b>Решение:</b>\n"
        "• 5-шаговый интерактивный квиз в Telegram с расчетом сметы ремонта/подбором ЖК;\n"
        "• Прогрев кейсами студии прямо перед выдачей расчета;\n"
        "• Менеджер получает горячего клиента с известным бюджетом, площадью и сроками.\n\n"
        "📈 <b>Результат:</b>\n"
        "• Стоимость целевого квалифицированного контакта снизилась до <b>540 ₽</b>;\n"
        "• Конверсия звонка в замер/встречу выросла почти в 2 раза."
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_single_case_kb(), parse_mode="HTML")
    await call.answer()

# ────────────────────────── РАЗДЕЛ ТАРИФОВ И УСЛУГ (ЕДИНЫЙ ЭКРАН) ──────────────────────────

@router.callback_query(F.data == "services_menu")
async def cb_services_menu(call: CallbackQuery):
    text = (
        "📂 <b>ТАРИФЫ И РЕШЕНИЯ // PXLBOT STUDIOS</b>\n"
        + DIVIDER +
        "Разрабатываем на чистом кастомном коде (Python / React). Вы получаете <b>полную независимость</b>: "
        "бот навсегда принадлежит вам, без абонентской платы сторонним конструкторам.\n\n"
        "<b>Выберите подходящий формат работы:</b>\n\n"
        "🎁 <b>1. Комплекты «Всё включено» (Выгода до 30%)</b>\n"
        "<i>Разработка + Техподдержка (включая сервер в РФ) + Продающие рассылки по вашей базе. "
        "Один договор, фиксированная цена на квартал или полгода вперед.</i>\n\n"
        "⚙️ <b>2. Базовая разработка по модулям (от 25 000 ₽)</b>\n"
        "<i>Индивидуальная разработка под ключ (Квиз-воронка, Каталог с оплатой или Mini App). "
        "В каждый проект уже включено 15 дней техподдержки и сервера бесплатно*.</i>\n\n"
        "🛡 <b>3. Техподдержка и сервер (от 5 900 ₽/мес)</b>\n"
        "<i>Предоставление защищенного VPS в РФ (152-ФЗ), мониторинг 24/7, ежедневные бэкапы "
        "и включенные часы работы инженера на правки по вашей заявке.</i>\n\n"
        "<i>*При подключении любого тарифа техподдержки: первые 15 дней бесплатны со дня сдачи проекта.</i>\n\n"
        "👇 Выберите нужный раздел ниже или рассчитайте точную смету:"
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_services_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "modules_menu")
async def cb_modules_menu(call: CallbackQuery):
    text = (
        "⚙️ <b>БАЗОВАЯ РАЗРАБОТКА ПО МОДУЛЯМ</b>\n"
        + DIVIDER +
        "Каждое решение создается на чистом коде под задачи вашего бизнеса:\n\n"
        "🟢 <b>1. Пакет «Быстрый поток заявок 24/7» — 25 000 – 40 000 ₽</b>\n"
        "<i>Для услуг, ремонта, автобизнеса, медицины, недвижимости и B2B</i>\n"
        "• Интерактивная квиз-воронка, расчет цены и квалификация лида за 30 секунд\n"
        "• Отсекает нецелевых и передает горячий контакт с параметрами в Telegram/CRM\n"
        "• Базовый юридический контур по 152-ФЗ (согласие на обработку данных)\n"
        "• ⏱ <b>Срок запуска:</b> 3–5 дней | 🎁 <b>15 дней техподдержки в подарок*</b>\n\n"
        "🔵 <b>2. Пакет «Автономный отдел продаж» — 50 000 – 85 000 ₽</b> <i>(Хит)</i>\n"
        "<i>Для интернет-магазинов, селлеров, опта, онлайн-школ и регулярных услуг</i>\n"
        "• Каталог товаров/услуг с фильтрами, корзиной, приемом оплат (СБП/карты) и чеками\n"
        "• Двухсторонняя интеграция с CRM (AmoCRM / Bitrix24) и складом (МойСклад)\n"
        "• Удобная админ-панель для управления товарами, заказами и базой клиентов\n"
        "• ⏱ <b>Срок запуска:</b> 7–14 дней | 🎁 <b>15 дней техподдержки в подарок*</b>\n\n"
        "🟣 <b>3. Пакет «Цифровая экосистема / Mini App» — 95 000 – 190 000 ₽</b>\n"
        "<i>Для стартапов, сетей, маркетплейсов и сервисов с личным кабинетом</i>\n"
        "• Полноценное мобильное приложение прямо внутри Telegram (React + Python Backend)\n"
        "• Интерфейс как в AppStore, но открывается мгновенно и без риска удалений\n"
        "• Личный кабинет, клубная подписка, сложная логика и высокая скорость\n"
        "• ⏱ <b>Срок запуска:</b> 2–4 недели | 🎁 <b>15 дней техподдержки в подарок*</b>\n\n"
        "<i>*При подключении любого тарифа техподдержки: 15 дней бесплатно со дня сдачи проекта.</i>\n\n"
        "👇 Рассчитайте точную смету или изучите комплекты «Всё включено»:"
    )
    await call.message.edit_text(text=text, reply_markup=get_modules_kb(), parse_mode="HTML")
    await call.answer()

# ────────────────────────── РАЗДЕЛ КОМПЛЕКСНЫХ ПАКЕТОВ (BUNDLES) ──────────────────────────

@router.callback_query(F.data == "bundles_menu")
async def cb_bundles_menu(call: CallbackQuery):
    text = (
        "🎁 <b>КОМПЛЕКТЫ «ВСЁ ВКЛЮЧЕНО» // ВЫГОДА ДО 30%</b>\n"
        + DIVIDER +
        "Формат для бизнеса, которому нужен готовый результат под ключ:\n"
        "<b>Разработка + Техподдержка (включая сервер в РФ) + Продающие рассылки по вашей базе.</b>\n\n"
        "Один фиксированный договор на 3–6 месяцев. Никаких непредвиденных доплат за хостинг или правки.\n\n"
        "<b>В каждый комплект входит:</b>\n"
        "• Разработка кастомного бота на чистом коде под вашу нишу;\n"
        "• Предоставление защищенного VPS-сервера в РФ (152-ФЗ) на весь срок;\n"
        "• Техподдержка: бэкапы, мониторинг 24/7 и часы работы инженера на правки по вашей заявке;\n"
        "• Промо-рассылки по вашей базе клиентов с маркировкой рекламы ОРД/erid по закону.\n\n"
        "<b>Выберите подходящий комплект для изучения состава и бронирования:</b>"
    )
    await call.message.edit_text(text=text, reply_markup=get_bundles_menu_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "bundle_start")
async def cb_bundle_start(call: CallbackQuery):
    b = BUNDLES_CATALOG["start"]
    text = (
        f"<b>{b['title']}</b>\n"
        + DIVIDER +
        f"💰 <b>Пакетная цена:</b> <code>{b['price']}</code> <s>{b['old_price']}</s>\n"
        f"🔥 <b>Ваша выгода:</b> <b>{b['economy']}</b> (скидка ~28%)\n"
        f"⏱ <b>Срок запуска:</b> {b['term']}\n"
        f"🛡 <b>Сервис:</b> {b['support']}\n\n"
        + b["desc"]
    )
    await call.message.edit_text(text=text, reply_markup=get_single_bundle_kb("start"), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "bundle_sales")
async def cb_bundle_sales(call: CallbackQuery):
    b = BUNDLES_CATALOG["sales"]
    text = (
        f"<b>{b['title']}</b>\n"
        + DIVIDER +
        f"💰 <b>Пакетная цена:</b> <code>{b['price']}</code> <s>{b['old_price']}</s>\n"
        f"🔥 <b>Ваша выгода:</b> <b>{b['economy']}</b> (скидка ~29%)\n"
        f"⏱ <b>Срок запуска:</b> {b['term']}\n"
        f"🛡 <b>Сервис:</b> {b['support']}\n\n"
        + b["desc"]
    )
    await call.message.edit_text(text=text, reply_markup=get_single_bundle_kb("sales"), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "bundle_pro")
async def cb_bundle_pro(call: CallbackQuery):
    b = BUNDLES_CATALOG["pro"]
    text = (
        f"<b>{b['title']}</b>\n"
        + DIVIDER +
        f"💰 <b>Пакетная цена:</b> <code>{b['price']}</code> <s>{b['old_price']}</s>\n"
        f"🔥 <b>Ваша выгода:</b> <b>{b['economy']}</b> (скидка ~36%)\n"
        f"⏱ <b>Срок запуска:</b> {b['term']}\n"
        f"🛡 <b>Сервис:</b> {b['support']}\n\n"
        + b["desc"]
    )
    await call.message.edit_text(text=text, reply_markup=get_single_bundle_kb("pro"), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data.startswith("order_bundle_"))
async def cb_order_bundle(call: CallbackQuery, state: FSMContext):
    bundle_code = call.data.replace("order_bundle_", "")
    b = BUNDLES_CATALOG.get(bundle_code, BUNDLES_CATALOG["sales"])
    await state.clear()
    await state.update_data(
        bundle_code=bundle_code,
        bundle_title=b["title"],
        bundle_price=b["price"]
    )
    await state.set_state(BundleOrderStates.entering_contact)

    text = (
        f"✍️ <b>БРОНИРОВАНИЕ: {b['title']}</b>\n"
        + DIVIDER +
        f"Спеццена: <b>{b['price']}</b> (экономия {b['economy']})\n\n"
        "Напишите ваше <b>Имя</b> и контакт для связи (Telegram @username или номер телефона).\n\n"
        "<i>Пример: Максим, @maxim_ceo, +7 999 123-45-67</i>"
    )
    await call.message.edit_text(text=text, reply_markup=get_cancel_kb(), parse_mode="HTML")
    await call.answer()

@router.message(BundleOrderStates.entering_contact)
async def process_bundle_contact(message: Message, state: FSMContext, bot: Bot):
    contact = message.text
    data = await state.get_data()
    bundle_title = data.get("bundle_title", "Комплект под ключ")
    bundle_price = data.get("bundle_price", "Не указана")
    await state.clear()

    await message.answer(
        f"✅ <b>Заявка на {bundle_title} принята!</b>\n"
        + DIVIDER +
        f"Спеццена {bundle_price} успешно зафиксирована за вами.\n"
        "Основатель студии (@Nicky_pxl) свяжется с вами в течение часа для согласования ТЗ и старта проекта.",
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

    target_admin_id = get_admin_id()
    if target_admin_id and target_admin_id != 0:
        admin_text = (
            "🔥 <b>НОВЫЙ ЗАКАЗ КОМПЛЕКТНОГО ПАКЕТА!</b>\n"
            + DIVIDER +
            f"📦 <b>Комплект:</b> {bundle_title}\n"
            f"💰 <b>Спеццена:</b> {bundle_price}\n"
            f"👤 <b>Клиент:</b> {contact}\n"
            f"📱 <b>От пользователя:</b> @{message.from_user.username or 'не указан'} (ID: <code>{message.from_user.id}</code>)"
        )
        try:
            await bot.send_message(chat_id=target_admin_id, text=admin_text, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка отправки уведомления админу: {e}")

# ────────────────────────── РАЗДЕЛ ТЕХПОДДЕРЖКИ, ГАРАНТИИ И ДАШБОРДА ──────────────────────────

@router.callback_query(F.data == "support_menu")
async def cb_support_menu(call: CallbackQuery):
    text = (
        "🛡 <b>ТЕХНИЧЕСКАЯ ПОДДЕРЖКА И СЕРВЕР // PXLBOT</b>\n"
        + DIVIDER +
        "Берем на себя всю техническую рутину: размещение на быстрых серверах в РФ, "
        "бесперебойную работу 24/7 и оперативные правки по вашей заявке.\n\n"
        "<b>Что входит в техподдержку:</b>\n"
        "• Предоставление защищенного сервера (VPS) на территории РФ (152-ФЗ);\n"
        "• Ежедневные резервные копии базы данных и мониторинг доступности 24/7;\n"
        "• Включенные часы работы инженера на замену цен, текстов, фото и доработку сценариев по вашей заявке;\n"
        "• В тарифах с рассылкой: подготовка и отправка промо-рассылок по вашей базе с маркировкой ОРД/erid.\n\n"
        "<b>Условия бесплатного периода:</b>\n"
        "• В каждый проект разработки включено <b>15 дней техподдержки и сервера бесплатно*</b>;\n"
        "• Во время разработки дни НЕ расходуются — отсчет начинается строго со дня сдачи готового бота;\n"
        "• Первый счет по тарифу выставляется только на 16-й день работы бота.\n\n"
        "👇 Выберите тариф техподдержки для изучения деталей или откройте свой дашборд:"
    )
    await call.message.edit_text(text=text, reply_markup=get_support_menu_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "support_status")
async def cb_support_status(call: CallbackQuery):
    user_id = call.from_user.id
    plan_info = get_user_plan_info(user_id)
    plan_key = plan_info.get("plan_key", "growth")
    plan_data = PLANS_CATALOG.get(plan_key, PLANS_CATALOG["growth"])

    text = (
        "📊 <b>ВАШ ДАШБОРД ТЕХПОДДЕРЖКИ И ГАРАНТИИ</b>\n"
        + DIVIDER +
        "🟢 <b>Статус:</b> 15 дней техподдержки и сервера включено бесплатно*\n"
        f"🛡 <b>Выбранный тариф:</b> {plan_data['title']}\n"
        "⏳ <b>Осталось дней:</b> 15 дней (активируются в момент сдачи бота)\n"
        "💳 <b>Следующая оплата:</b> Через 15 дней после релиза бота в работу\n"
        f"⚡️ <b>Скорость реакции инженера:</b> {plan_data['reaction']}\n"
        f"🛠 <b>Лимит работы инженера:</b> {plan_data['hours']}\n"
        "📡 <b>Персональный канал связи:</b> Чат с ведущим инженером (@Nicky_pxl)\n"
        "🔒 <b>Сервер:</b> Защищенный VPS в РФ (152-ФЗ) + авто-бэкапы каждые 24ч\n\n"
        "<i>*Во время разработки дни заморожены и начнут действовать "
        "только тогда, когда вы примете готового рабочего бота.</i>"
    )
    await call.message.edit_text(text=text, reply_markup=get_support_status_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "support_plan_base")
async def cb_plan_base(call: CallbackQuery):
    p = PLANS_CATALOG["base"]
    text = (
        f"🛡 <b>{p['title']}</b>\n"
        + DIVIDER +
        "<i>Идеально для квиз-воронок и лид-ботов без частых изменений логики.</i>\n\n"
        "<b>Что входит в тариф:</b>\n"
        "• Размещение на быстром защищенном сервере в РФ (соответствие 152-ФЗ);\n"
        "• Ежедневные резервные копии базы данных и мониторинг аптайма 24/7;\n"
        f"• <b>{p['hours']}</b>: оперативная замена текстов, цен, фото, ссылок;\n"
        f"• Скорость реакции команды: <b>{p['reaction']}</b>.\n\n"
        "⏱ <b>Первые 15 дней — бесплатно</b> при заказе любого бота в студии."
    )
    await call.message.edit_text(text=text, reply_markup=get_support_plan_detail_kb("base"), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "support_plan_growth")
async def cb_plan_growth(call: CallbackQuery):
    p = PLANS_CATALOG["growth"]
    text = (
        f"🚀 <b>{p['title']}</b>\n"
        + DIVIDER +
        "<i>Выбор 70% клиентов: для активного бизнеса с рекламой и CRM.</i>\n\n"
        "<b>Что входит в тариф:</b>\n"
        "• Все опции тарифа «Базовый» + приоритетная реакция <b>до 1 часа 24/7</b>;\n"
        f"• <b>{p['hours']}</b>: доработка веток, интеграций, докрутка сценариев по вашей заявке;\n"
        "• <b>+ 1 акционная/прогревающая рассылка в месяц «под ключ»</b> по базе ваших пользователей;\n"
        "• Маркировка рекламы при отправке рассылок (токены <code>erid</code> / ОРД / 152-ФЗ);\n"
        "• Персональный инженер на связи в рабочем чате.\n\n"
        "⏱ <b>Первые 15 дней — бесплатно</b> при сдаче бота."
    )
    await call.message.edit_text(text=text, reply_markup=get_support_plan_detail_kb("growth"), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "support_plan_pro")
async def cb_plan_pro(call: CallbackQuery):
    p = PLANS_CATALOG["pro"]
    text = (
        f"💎 <b>{p['title']}</b>\n"
        + DIVIDER +
        "<i>Выделенный IT-отдел для Telegram Mini Apps, маркетплейсов и стартапов.</i>\n\n"
        "<b>Что входит в тариф:</b>\n"
        "• Выделенный сервер под высокую нагрузку (Stage + Production);\n"
        f"• Экстренная реакция команды: <b>{p['reaction']}</b>;\n"
        f"• <b>{p['hours']}</b> на внедрение новых экранов, механик и фич;\n"
        "• До 3 сегментированных рассылок в месяц с технической маркировкой ОРД/erid;\n"
        "• Прямой приоритетный канал связи с разработчиком.\n\n"
        "⏱ <b>Первые 15 дней — бесплатно</b> при сдаче бота."
    )
    await call.message.edit_text(text=text, reply_markup=get_support_plan_detail_kb("pro"), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data.startswith("select_plan_"))
async def cb_select_plan(call: CallbackQuery):
    plan_code = call.data.replace("select_plan_", "")
    user_id = call.from_user.id
    set_user_plan(user_id, plan_code)
    plan_data = PLANS_CATALOG.get(plan_code, PLANS_CATALOG["growth"])

    text = (
        f"✅ <b>Тариф успешно выбран: {plan_data['title']}!</b>\n"
        + DIVIDER +
        "Ваш выбор зафиксирован в системе студии.\n\n"
        "🟢 <b>Статус:</b> 15 дней техподдержки включены в ваш проект.\n"
        "⏳ <b>Активация:</b> ровно в день сдачи готового бота в эксплуатацию.\n"
        "💳 <b>Первая оплата тарифа:</b> только по завершении 15 бесплатных дней.\n"
        "📡 <b>Канал связи:</b> чат с инженером @Nicky_pxl уже доступен.\n\n"
        "Нажмите кнопку ниже, чтобы проверить ваш обновленный дашборд:"
    )
    await call.message.edit_text(text=text, reply_markup=get_support_status_kb(), parse_mode="HTML")
    await call.answer("Тариф успешно выбран!")

@router.callback_query(F.data == "start_support_audit")
async def cb_start_support_audit(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(SupportAuditStates.entering_bot_link)
    text = (
        "🚑 <b>РЕАНИМАЦИЯ / ПЕРЕНОС СУЩЕСТВУЮЩЕГО БОТА</b>\n"
        + DIVIDER +
        "Разработчик пропал, упал сервер, нужно обновить прайс или перенести бота с конструктора на надежный код?\n\n"
        "Отправьте <b>ссылку/@username вашего бота</b> и кратко опишите, что сейчас не работает или требует доработки:"
    )
    await call.message.edit_text(text=text, reply_markup=get_cancel_kb(), parse_mode="HTML")
    await call.answer()

@router.message(SupportAuditStates.entering_bot_link)
async def process_support_bot_link(message: Message, state: FSMContext):
    await state.update_data(bot_info=message.text)
    await state.set_state(SupportAuditStates.entering_contact)
    text = (
        "👍 Принято! Теперь укажите ваше <b>Имя</b> и контакт для связи (Telegram @username или телефон), "
        "чтобы ведущий инженер провел экспресс-диагностику и прислал план восстановления:"
    )
    await message.answer(text=text, reply_markup=get_cancel_kb(), parse_mode="HTML")

@router.message(SupportAuditStates.entering_contact)
async def process_support_contact(message: Message, state: FSMContext, bot: Bot):
    contact = message.text
    data = await state.get_data()
    bot_info = data.get("bot_info", "Не указано")
    await state.clear()

    await message.answer(
        "✅ <b>Заявка на диагностику принята!</b>\n"
        + DIVIDER +
        "Ведущий инженер студии проверит бота и свяжется с вами в течение часа с планом запуска и рекомендациями.",
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

    target_admin_id = get_admin_id()
    if target_admin_id and target_admin_id != 0:
        admin_text = (
            "🚑 <b>ЗАЯВКА НА ПОЧИНКУ / ТЕХПОДДЕРЖКУ БОТА</b>\n"
            + DIVIDER +
            f"👤 <b>Контакты:</b> {contact}\n"
            f"📱 <b>От:</b> @{message.from_user.username or 'не указан'} (ID: <code>{message.from_user.id}</code>)\n\n"
            f"🤖 <b>Бот и описание задачи:</b>\n{bot_info}"
        )
        try:
            await bot.send_message(chat_id=target_admin_id, text=admin_text, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка отправки уведомления админу: {e}")

# ────────────────────────── РАЗДЕЛ О СТУДИИ (B2B // ПРЕЗЕНТАЦИЯ) ──────────────────────────

@router.callback_query(F.data.in_(["about_menu", "venture_menu"]))
async def cb_about_menu(call: CallbackQuery):
    text = (
        "💼 <b>О СТУДИИ PXLBOT STUDIOS</b>\n"
        + DIVIDER +
        "<b>Инженерная студия и продуктовая лаборатория Telegram Mini Apps, ботов и B2B-автоматизаций.</b>\n\n"
        "Мы превращаем Telegram в полноценный автономный канал продаж и управления бизнесом — от быстрых лид-воронок до масштабных экосистем с онлайн-оплатой и личными кабинетами.\n\n"
        "<b>Почему бизнесу выгодно работать с нами:</b>\n"
        "• <b>Разработка в коде, а не на конструкторах:</b> пишем на надежном стеке (Python / Aiogram / FastAPI / React). Код полностью принадлежит вам и размещается на быстрых защищенных VPS в РФ.\n"
        "• <b>Фокус на окупаемость (ROMI):</b> проектируем путь клиента (CJM), связываем систему с AmoCRM, Bitrix24, МойСклад и подключаем онлайн-кассы по 54-ФЗ.\n"
        "• <b>Юридический контур:</b> работаем официально по договору, NDA, с соблюдением 152-ФЗ и маркировкой рекламы в рассылках (ОРД / erid по 347-ФЗ).\n"
        "• <b>15 дней техподдержки и серверов в подарок:</b> сопровождаем запуск, мониторим аптайм 24/7 и оперативно вносим правки по вашей заявке.\n\n"
        "<b>Материалы и знакомство в нашем Telegram-канале:</b>\n"
        "🧭 <a href=\"https://t.me/pxlbot_studios/10\">Пост «Навигация»</a> — гид по каналу и решениям\n"
        "👥 <a href=\"https://t.me/pxlbot_studios/11\">Пост «Команда»</a> — кто создает архитектуру и отвечает за результат\n"
        "⚡️ <a href=\"https://t.me/pxlbot_studios/13\">Пост «Экспертиза»</a> — стандарты разработки и надежность\n\n"
        "💬 <b>Основатель студии:</b> @Nicky_pxl — на связи для персональных консультаций и разбора задач вашего бизнеса."
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_about_kb(), parse_mode="HTML", disable_web_page_preview=True)
    await call.answer()

# ────────────────────────── ТОЧНЫЙ 4-ШАГОВЫЙ КАЛЬКУЛЯТОР ──────────────────────────

@router.callback_query(F.data == "start_calc")
async def cb_start_calc(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(CalculatorStates.choosing_product)
    text = (
        "🧮 <b>ИНТЕРАКТИВНЫЙ КАЛЬКУЛЯТОР // ШАГ 1 ИЗ 4</b>\n"
        + DIVIDER +
        "Какой базовый формат решения вам требуется?"
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_calc_product_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(CalculatorStates.choosing_product, F.data.startswith("calc_prod_"))
async def cb_calc_prod(call: CallbackQuery, state: FSMContext):
    prod_type = call.data.replace("calc_prod_", "")
    await state.update_data(product=prod_type)
    await state.set_state(CalculatorStates.choosing_niche)

    text = (
        "🧮 <b>ИНТЕРАКТИВНЫЙ КАЛЬКУЛЯТОР // ШАГ 2 ИЗ 4</b>\n"
        + DIVIDER +
        "В какой сфере работает ваш бизнес?"
    )
    await call.message.edit_text(text=text, reply_markup=get_calc_niche_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(CalculatorStates.choosing_niche, F.data.startswith("calc_niche_"))
async def cb_calc_niche(call: CallbackQuery, state: FSMContext):
    niche = call.data.replace("calc_niche_", "")
    await state.update_data(niche=niche)
    await state.set_state(CalculatorStates.choosing_integration)

    text = (
        "🧮 <b>ИНТЕРАКТИВНЫЙ КАЛЬКУЛЯТОР // ШАГ 3 ИЗ 4</b>\n"
        + DIVIDER +
        "Какой контур интеграций вам требуется?"
    )
    await call.message.edit_text(text=text, reply_markup=get_calc_integration_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(CalculatorStates.choosing_integration, F.data.startswith("calc_int_"))
async def cb_calc_int(call: CallbackQuery, state: FSMContext):
    integration = call.data.replace("calc_int_", "")
    await state.update_data(integration=integration)
    await state.set_state(CalculatorStates.choosing_addon)

    text = (
        "🧮 <b>ИНТЕРАКТИВНЫЙ КАЛЬКУЛЯТОР // ШАГ 4 ИЗ 4</b>\n"
        + DIVIDER +
        "Требуются ли дополнительные модули усиления конверсии?"
    )
    await call.message.edit_text(text=text, reply_markup=get_calc_addon_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(CalculatorStates.choosing_addon, F.data.startswith("calc_add_"))
async def cb_calc_addon(call: CallbackQuery, state: FSMContext):
    addon = call.data.replace("calc_add_", "")
    data = await state.get_data()

    prod_key = data.get("product", "quizbot")
    niche_key = data.get("niche", "other")
    int_key = data.get("integration", "none")

    prod_data = CALC_PRODUCTS.get(prod_key, CALC_PRODUCTS["quizbot"])
    niche_title = CALC_NICHES.get(niche_key, "Другая сфера")
    int_data = CALC_INTEGRATIONS.get(int_key, CALC_INTEGRATIONS["none"])
    addon_data = CALC_ADDONS.get(addon, CALC_ADDONS["none"])

    base_price = prod_data["price"]
    int_price = int_data["price"]
    addon_price = addon_data["price"]
    total_price = base_price + int_price + addon_price

    base_days = prod_data["days"]
    int_days = int_data["days"]
    addon_days = addon_data["days"]
    total_days = base_days + int_days + addon_days
    days_str = f"{max(2, total_days - 1)}–{total_days + 2} рабочих дней"

    if total_price <= 45000:
        rec_support = "Тариф «Базовый» — 5 900 ₽/мес"
        bundle_hint = (
            "💡 <i>Спецпредложение: данный проект доступен в комплекте «Быстрый старт 360°» "
            "с 3 мес. сервера и техподдержки всего за 39 900 ₽ (раздел Комплекты).</i>\n\n"
        )
    elif total_price <= 90000:
        rec_support = "Тариф «Развитие + Рассылка» — 12 900 ₽/мес (Хит продаж)"
        bundle_hint = (
            "💡 <i>Спецпредложение: доступен комплект «Турбо-продажи + Маркетинг» за 89 000 ₽ "
            "(с 3 мес. техподдержки, сервером и 3 готовыми рассылками под ключ).</i>\n\n"
        )
    else:
        rec_support = "Тариф «Выделенный IT-отдел» — 24 900 ₽/мес"
        bundle_hint = (
            "💡 <i>Спецпредложение: доступен комплект «Digital-Экосистема PRO» за 199 000 ₽ "
            "(с 6 мес. техподдержки, выделенным сервером и доработками).</i>\n\n"
        )

    int_price_str = f"+{int_price:,} ₽".replace(",", " ") if int_price > 0 else "включено (0 ₽)"
    addon_price_str = f"+{addon_price:,} ₽".replace(",", " ") if addon_price > 0 else "не выбрано (0 ₽)"
    total_price_str = f"{total_price:,} ₽".replace(",", " ")

    await state.update_data(
        final_product=prod_data["title"],
        final_prod_price=f"{base_price:,} ₽".replace(",", " "),
        final_niche=niche_title,
        final_int=int_data["title"],
        final_int_price=int_price_str,
        final_addon=addon_data["title"],
        final_addon_price=addon_price_str,
        price_total=total_price_str,
        days=days_str,
        rec_support=rec_support
    )

    text = (
        "📊 <b>ТОЧНЫЙ РАСЧЕТ СМЕТЫ ПРОЕКТА</b>\n"
        + DIVIDER +
        f"• <b>Базовое решение:</b> {prod_data['title']} — <code>{base_price:,} ₽</code>\n".replace(",", " ")
        + f"• <b>Сфера бизнеса:</b> {niche_title}\n"
        f"• <b>Интеграции:</b> {int_data['title']} — <code>{int_price_str}</code>\n"
        f"• <b>Доп. модуль:</b> {addon_data['title']} — <code>{addon_price_str}</code>\n"
        + DIVIDER +
        f"💰 <b>ИТОГОВАЯ ТОЧНАЯ СМЕТА:</b> <code>{total_price_str}</code>\n"
        f"⏱ <b>Срок сдачи проекта:</b> {days_str}\n\n"
        "🎁 <b>Что уже входит в стоимость:</b>\n"
        "✅ 100% чистый код навсегда (без абонентки конструкторам)\n"
        "✅ Базовый юридический контур по 152-ФЗ\n"
        "✅ <b>15 дней сервера и техподдержки БЕСПЛАТНО!*</b>\n\n"
        f"🛡 <b>Рекомендуемая техподдержка (с 16-го дня):</b>\n"
        f"<code>{rec_support}</code>\n\n"
        f"{bundle_hint}"
        "Зафиксируйте расчет, чтобы забронировать срок за студией и получить официальное КП:"
    )

    await call.message.edit_text(text=text, reply_markup=get_calc_result_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "calc_submit_order")
async def cb_calc_submit(call: CallbackQuery, state: FSMContext):
    await state.set_state(CalculatorStates.entering_contact)
    text = (
        "✍️ <b>ФИКСАЦИЯ СМЕТЫ И ПОЛУЧЕНИЕ КП</b>\n"
        + DIVIDER +
        "Напишите ваше <b>Имя</b> и контакт для связи (Telegram @username или номер телефона).\n\n"
        "<i>Пример: Сергей, @sergey_ceo, +7 999 123-45-67</i>"
    )
    await call.message.edit_text(text=text, reply_markup=get_cancel_kb(), parse_mode="HTML")
    await call.answer()

@router.message(CalculatorStates.entering_contact)
async def process_calc_contact(message: Message, state: FSMContext, bot: Bot):
    contact = message.text
    data = await state.get_data()
    await state.clear()

    await message.answer(
        "✅ <b>Точная смета успешно зафиксирована!</b>\n"
        + DIVIDER +
        "Основатель студии (@Nicky_pxl) уже получил детали вашего расчета "
        "и свяжется с вами с готовым коммерческим предложением и договором.",
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

    target_admin_id = get_admin_id()
    if target_admin_id and target_admin_id != 0:
        admin_text = (
            "🚨 <b>НОВАЯ ЗАЯВКА ИЗ КАЛЬКУЛЯТОРА (ТОЧНЫЙ РАСЧЕТ)</b>\n"
            + DIVIDER +
            f"👤 <b>Клиент:</b> {contact}\n"
            f"📱 <b>От:</b> @{message.from_user.username or 'не указан'} (ID: <code>{message.from_user.id}</code>)\n\n"
            f"📦 <b>Движок:</b> {data.get('final_product')} ({data.get('final_prod_price')})\n"
            f"🏢 <b>Ниша:</b> {data.get('final_niche')}\n"
            f"🔌 <b>Интеграции:</b> {data.get('final_int')} ({data.get('final_int_price')})\n"
            f"➕ <b>Доп. модуль:</b> {data.get('final_addon')} ({data.get('final_addon_price')})\n"
            + DIVIDER +
            f"💰 <b>ИТОГО СМЕТА:</b> {data.get('price_total')}\n"
            f"⏱ <b>СРОК:</b> {data.get('days')}\n"
            f"🛡 <b>ТЕХПОДДЕРЖКА:</b> {data.get('rec_support')}"
        )
        try:
            await bot.send_message(chat_id=target_admin_id, text=admin_text, parse_mode="HTML")
            
            # Генерация и отправка официальной сметы Word (Приложение №1)
            if generate_smeta_docx:
                try:
                    smeta_file_path = generate_smeta_docx(data, client_contact=contact)
                    client_tag = (message.from_user.username or f"id{message.from_user.id}").replace("@", "")
                    doc_file = FSInputFile(smeta_file_path, filename=f"Приложение_1_Смета_PxlBot_{client_tag}.docx")
                    await bot.send_document(
                        chat_id=target_admin_id,
                        document=doc_file,
                        caption=(
                            "📄 <b>Официальная смета (Приложение №1 к Договору)</b>\n"
                            f"Сформирована для: <b>{contact}</b>\n"
                            f"Итоговая сумма: <b>{data.get('price_total')}</b>\n"
                            "<i>(Файл отправлен только вам как администратору)</i>"
                        ),
                        parse_mode="HTML"
                    )
                except Exception as docx_err:
                    print(f"Ошибка формирования файла сметы: {docx_err}")
        except Exception as e:
            print(f"Ошибка отправки уведомления или сметы админу: {e}")

# ────────────────────────── ПРЯМАЯ ЗАЯВКА НА РАЗРАБОТКУ ──────────────────────────

@router.callback_query(F.data == "start_order")
async def cb_start_order(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(OrderStates.entering_details)
    text = (
        "📝 <b>ОБСУДИТЬ ПРОЕКТ // PXLBOT STUDIOS</b>\n"
        + DIVIDER +
        "Опишите в 1–2 предложениях: какая у вас сфера бизнеса и какую задачу нужно решить ботом?"
    )
    await safe_send_or_edit(call, text=text, reply_markup=get_cancel_kb(), parse_mode="HTML")
    await call.answer()

@router.message(OrderStates.entering_details)
async def process_order_details(message: Message, state: FSMContext):
    await state.update_data(details=message.text)
    await state.set_state(OrderStates.entering_contact)
    text = (
        "👍 Отлично! Теперь напишите ваше <b>Имя</b> и контакт для связи (Telegram @username или телефон):"
    )
    await message.answer(text=text, reply_markup=get_cancel_kb(), parse_mode="HTML")

@router.message(OrderStates.entering_contact)
async def process_order_contact(message: Message, state: FSMContext, bot: Bot):
    contact = message.text
    data = await state.get_data()
    task = data.get("details", "Не указано")
    await state.clear()

    await message.answer(
        "✅ <b>Заявка принята!</b>\n"
        + DIVIDER +
        "Основатель PxlBot Studios (@Nicky_pxl) свяжется с вами в течение часа для экспресс-разбора.",
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

    target_admin_id = get_admin_id()
    if target_admin_id and target_admin_id != 0:
        admin_text = (
            "🔥 <b>ПРЯМАЯ ЗАЯВКА В PXLBOT STUDIOS!</b>\n"
            + DIVIDER +
            f"👤 <b>Контакты:</b> {contact}\n"
            f"📱 <b>От:</b> @{message.from_user.username or 'не указан'} (ID: <code>{message.from_user.id}</code>)\n\n"
            f"📋 <b>Задача клиента:</b>\n{task}"
        )
        try:
            await bot.send_message(chat_id=target_admin_id, text=admin_text, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка отправки уведомления админу: {e}")

# ────────────────────────── АДМИН-ЗАГРУЗКА ВИДЕО КЕЙСОВ ──────────────────────────

@router.message(F.video)
async def handle_admin_video_upload(message: Message):
    save_admin_id_if_founder(message.from_user)
    admin_id = get_admin_id()
    sender_uname = (message.from_user.username or "").lower()
    is_admin = (
        message.from_user.id == admin_id
        or (admin_id == 0 and sender_uname == (FOUNDER_USERNAME or "nicky_pxl").lower())
        or sender_uname == (FOUNDER_USERNAME or "nicky_pxl").lower()
    )
    if is_admin:
        file_id = message.video.file_id
        set_cached_media("legal_video_file_id", file_id)
        size_mb = (message.video.file_size or 0) / (1024 * 1024)
        duration_sec = message.video.duration or 0
        await message.reply(
            f"📹 <b>Видео успешно получено и сохранено в облаке Telegram!</b>\n"
            + DIVIDER +
            f"🆔 <b>file_id:</b> <code>{file_id}</code>\n"
            f"📦 <b>Размер:</b> {size_mb:.1f} МБ\n"
            f"⏱ <b>Длительность:</b> {duration_sec} сек\n\n"
            f"✅ <b>Видео автоматически привязано к кейсу «ЮрБиржа»!</b>\n"
            f"Теперь любой пользователь в боте будет моментально получать это видео прямо из облака Telegram без задержек и ограничений по размеру.",
            parse_mode="HTML"
        )
