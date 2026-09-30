from aiogram import Router, F, Bot
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext

from keyboards import (
    get_main_menu_kb,
    get_cases_kb,
    get_single_case_kb,
    get_services_kb,
    get_support_kb,
    get_venture_kb,
    get_calc_product_kb,
    get_calc_niche_kb,
    get_calc_integration_kb,
    get_calc_result_kb,
    get_cancel_kb
)
from states import CalculatorStates, OrderStates, SupportAuditStates
from config import ADMIN_ID, FOUNDER_USERNAME
import os

router = Router()

DYNAMIC_ADMIN_FILE = "admin_id.txt"

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

MAIN_WELCOME_TEXT = (
    "👾 <b>PXLBOT STUDIOS // DIGITAL PRODUCTION & VENTURE BUILDER</b>\n"
    "────────────────────────────\n"
    "Инженерная студия разработки продающих систем в Telegram и Web.\n\n"
    "За каждым проектом закреплен пул из 6 профильных специалистов:\n"
    "<code>Backend • Frontend • UI/UX • Marketing • Legal (ЕАПК) • PM (MBA)</code>\n\n"
    "<b>Что мы создаем и развиваем:</b>\n"
    "• Конверсионные квиз-воронки и лид-боты\n"
    "• Бизнес-боты с CRM, эквайрингом и ИИ\n"
    "• Полноценные <b>Telegram Mini Apps (WebApp)</b>\n"
    "• Ежемесячное SLA-сопровождение, Growth-маркетинг и юр. защита (152-ФЗ / ОРД)\n\n"
    "👇 Выберите нужный раздел ниже:"
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
    await call.message.edit_text(
        text=MAIN_WELCOME_TEXT,
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )
    await call.answer()

# ────────────────────────── РАЗДЕЛ ПРОЕКТОВ И КЕЙСОВ ──────────────────────────

@router.callback_query(F.data == "cases_menu")
async def cb_cases_menu(call: CallbackQuery):
    text = (
        "🚀 <b>ПРОЕКТЫ И КЕЙСЫ // PXLBOT STUDIOS</b>\n"
        "────────────────────────────\n"
        "Мы не просто пишем код по ТЗ — мы создаем собственные сложные отраслевые платформы "
        "в формате <b>Telegram Mini Apps</b> и внедряем эти же технологии нашим клиентам.\n\n"
        "Выберите проект ниже, чтобы посмотреть архитектуру и бизнес-результат:"
    )
    await call.message.edit_text(text=text, reply_markup=get_cases_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "case_agro")
async def cb_case_agro(call: CallbackQuery):
    text = (
        "🌾 <b>ФЛАГМАН: «Агротерминал» & «Агротрейд» (AgroTech TMA)</b>\n"
        "────────────────────────────\n"
        "<b>Формат:</b> Собственная B2B-платформа студии (Telegram Mini App + Web)\n\n"
        "<b>Задача рынка:</b>\n"
        "Оцифровать рынок зерновых и масличных культур РФ, убрав хаос WhatsApp-чатов "
        "и цепочки посредников между фермерами и экспортерами.\n\n"
        "<b>Что реализовано в коде (React + TypeScript + TMA):</b>\n"
        "• <b>Агротерминал:</b> живые индексы и свечные графики TradingView по базисам "
        "<code>CPT Новороссийск / Тамань / Ростов</code> и <code>EXW Элеваторы</code>, пересчет RUB/USD и НДС, индикатор экспортной пошлины РФ.\n"
        "• <b>Калькулятор Netback («EXW Ангар»):</b> мгновенный расчет чистой цены тонны в хозяйстве "
        "с вычетом логистики (авто/ж/д) и рефакций за качество (протеин, влага, сор).\n"
        "• <b>Агротрейд (Order Book):</b> биржевой стакан прямых закупочных заявок от федеральных экспортеров "
        "и МЭЗов с фиксацией объема и цены в 1 клик.\n\n"
        "💡 <i>Хотите подобный B2B-терминал, калькулятор или торговую площадку для своей отрасли?</i>"
    )
    await call.message.edit_text(text=text, reply_markup=get_single_case_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "case_legal")
async def cb_case_legal(call: CallbackQuery):
    text = (
        "⚖️ <b>ФЛАГМАН: «ЮрБиржа» (LegalTech Marketplace & Escrow TMA)</b>\n"
        "────────────────────────────\n"
        "<b>Формат:</b> Собственная двухсторонняя платформа студии (Telegram Mini App)\n\n"
        "<b>Задача рынка:</b>\n"
        "Создать прозрачный маркетплейс юридических услуг (<code>Заказчик ↔ Юрист</code>) "
        "с защитой денег клиента и жестким фильтром квалификации исполнителей.\n\n"
        "<b>Что реализовано в коде:</b>\n"
        "• <b>Интерактивный квиз-брифинг и сравнение офферов:</b> клиент за 1 минуту формирует задачу "
        "и сравнивает предложения юристов на одном экране по цене, срокам и рейтингу.\n"
        "• <b>Безопасная сделка (Escrow) и Комната сделки:</b> резервирование средств и выплата "
        "только после нажатия кнопки «Принять работу» + независимый арбитраж за 48 часов.\n"
        "• <b>KYC и SaaS-монетизация:</b> верификация дипломов через ФИС ФРДО и Минюст РФ, "
        "система менторства и биллинг подписок (<code>PRO / PRO+</code>) со снижением комиссии с 15% до 8%.\n\n"
        "💡 <i>Разрабатываем двухсторонние биржи, сервисы услуг и личные кабинеты внутри Telegram под ключ.</i>"
    )
    await call.message.edit_text(text=text, reply_markup=get_single_case_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "case_miniapp")
async def cb_case_miniapp(call: CallbackQuery):
    text = (
        "🛍 <b>КЕЙС: E-commerce каталог и магазин в Telegram (Mini App)</b>\n"
        "────────────────────────────\n"
        "<b>Проблема:</b>\n"
        "Внешний сайт долго грузился с мобильного трафика, до 60% покупателей бросали корзину, "
        "а разработка мобильного приложения для iOS/Android стоила от 600 000 ₽.\n\n"
        "<b>Решение PxlBot Studios:</b>\n"
        "• Полноценное Web-приложение (Telegram Mini App) с открытием за 0.5 секунды прямо в чате;\n"
        "• Витрина с фильтрами, карточками товаров, корзиной и избранным;\n"
        "• Оплата через СБП / ЮKassa и авто-выгрузка заказа в CRM и МойСклад;\n"
        "• Юридическая упаковка оферты и согласий по 152-ФЗ.\n\n"
        "📈 <b>Результат:</b>\n"
        "• Конверсия в оплаченный заказ выросла в <b>2.4 раза</b>;\n"
        "• Экономия бюджета в <b>5–7 раз</b> по сравнению с классическим приложением."
    )
    await call.message.edit_text(text=text, reply_markup=get_single_case_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "case_auto")
async def cb_case_auto(call: CallbackQuery):
    text = (
        "🚗 <b>КЕЙС: Автобизнес, детейлинг и сервис</b>\n"
        "────────────────────────────\n"
        "<b>Проблема:</b>\n"
        "Мастера-приемщики тратили по 3 часа в день на однотипные вопросы в чатах и по телефону: "
        "«Сколько стоит комплекс / ТО на мою модель авто?».\n\n"
        "<b>Решение PxlBot Studios:</b>\n"
        "• Интерактивный бот-калькулятор с выбором кузова/класса авто и пакета услуг;\n"
        "• Мгновенный расчет сметы и бронирование свободного бокса;\n"
        "• Выгрузка готовой карточки клиента в CRM с номером телефона и параметрами авто.\n\n"
        "📈 <b>Результат:</b>\n"
        "• Время обработки обращения сократилось с 15 минут до <b>20 секунд</b>;\n"
        "• Рост конверсии в заезд на <b>+42%</b>."
    )
    await call.message.edit_text(text=text, reply_markup=get_single_case_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "case_beauty")
async def cb_case_beauty(call: CallbackQuery):
    text = (
        "💈 <b>КЕЙС: Клиника и сеть сферы услуг (Запись 24/7)</b>\n"
        "────────────────────────────\n"
        "<b>Проблема:</b>\n"
        "До 35% обращений с рекламы приходили вечером после 20:00 и терялись до утра. "
        "Высокий процент неявок по первичным записям.\n\n"
        "<b>Решение PxlBot Studios:</b>\n"
        "• Бот круглосуточной записи и первичной квалификации клиента за 4 клика;\n"
        "• Каскад автоматических напоминаний за 24 часа и за 2 часа до визита;\n"
        "• Автоматический сбор отзывов и возврат спящей базы через акционные рассылки.\n\n"
        "📈 <b>Результат:</b>\n"
        "• <b>+28% записей</b> на том же рекламном бюджете;\n"
        "• Снижение неявок (No-Show) на <b>65%</b>."
    )
    await call.message.edit_text(text=text, reply_markup=get_single_case_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "case_quiz")
async def cb_case_quiz(call: CallbackQuery):
    text = (
        "📋 <b>КЕЙС: Квиз-воронка для недвижимости и ремонта</b>\n"
        "────────────────────────────\n"
        "<b>Проблема:</b>\n"
        "Холодный трафик с Яндекс.Директ и посевов на обычный сайт давал дорогие лиды по 2 200 ₽, "
        "многие номера телефонов оказывались нецелевыми.\n\n"
        "<b>Решение PxlBot Studios:</b>\n"
        "• Пошаговая квиз-воронка в Telegram с расчетом сметы/подбором объектов за 5 шагов;\n"
        "• Автоматический прогрев кейсами компании прямо внутри бота;\n"
        "• Передача верифицированного контакта в отдел продаж.\n\n"
        "📈 <b>Результат:</b>\n"
        "• Снижение стоимости квалифицированного лида с 2 200 ₽ до <b>540 ₽</b>;\n"
        "• Менеджеры звонят клиенту, уже зная площадь, бюджет и сроки."
    )
    await call.message.edit_text(text=text, reply_markup=get_single_case_kb(), parse_mode="HTML")
    await call.answer()

# ────────────────────────── РАЗДЕЛ УСЛУГ И ТАРИФОВ НА РАЗРАБОТКУ ──────────────────────────

@router.callback_query(F.data == "services_menu")
async def cb_services_menu(call: CallbackQuery):
    text = (
        "📂 <b>УСЛУГИ И ТАРИФЫ НА РАЗРАБОТКУ // PXLBOT STUDIOS</b>\n"
        "────────────────────────────\n"
        "Мы работаем на <b>35–40% выгоднее классических неповоротливых агентств</b> за счет собственных "
        "готовых модулей, но даем чистый кастомный код (без абонентки конструкторам!), дизайн и юристов.\n\n"
        "🟢 <b>1. Тариф «КВИЗ / ЛИД-БОТ» — 25 000 – 40 000 ₽</b>\n"
        "• Интерактивная квиз-воронка, квалификация лидов, прайс, портфолио и запись 24/7\n"
        "• Мгновенные уведомления о заявках в рабочий чат или Google Таблицы\n"
        "• Базовый пакет документов по 152-ФЗ (согласие на обработку ПДн в боте)\n"
        "• ⏱ <b>Срок:</b> 3–5 дней | 🎁 <b>14 дней сопровождения бесплатно</b>\n\n"
        "🔵 <b>2. Тариф «БИЗНЕС-БОТ + CRM / AI» — 50 000 – 85 000 ₽</b> <i>(Хит продаж)</i>\n"
        "• Сложная бизнес-логика, калькуляторы, каталог, реферальная система или AI-ассистент\n"
        "• Двухсторонняя интеграция с AmoCRM / Bitrix24 / МойСклад\n"
        "• Подключение онлайн-оплаты (СБП, ЮKassa, рекуррентные платежи) и админ-панель\n"
        "• ⏱ <b>Срок:</b> 7–14 дней | 🎁 <b>14 дней сопровождения бесплатно</b>\n\n"
        "🟣 <b>3. Тариф «TELEGRAM MINI APP (WebApp)» — 95 000 – 190 000 ₽</b>\n"
        "• Полноценное веб-приложение внутри Telegram (React + TypeScript + Python Backend)\n"
        "• Интернет-магазины, биржи, личные кабинеты, аналитические дашборды и калькуляторы\n"
        "• Уникальный UI/UX-дизайн, высокая нагрузка, эквайринг и полное юр. оформление\n"
        "• ⏱ <b>Срок:</b> 2–4 недели | 🎁 <b>14 дней сопровождения бесплатно</b>\n\n"
        "👇 Рассчитайте точную смету под вашу нишу в калькуляторе или изучите контур сопровождения:"
    )
    await call.message.edit_text(text=text, reply_markup=get_services_kb(), parse_mode="HTML")
    await call.answer()

# ────────────────────────── РАЗДЕЛ СОПРОВОЖДЕНИЯ И SLA (RETAINER) ──────────────────────────

@router.callback_query(F.data == "support_menu")
async def cb_support_menu(call: CallbackQuery):
    text = (
        "🛡 <b>СОПРОВОЖДЕНИЕ, РОСТ И SLA // PXLBOT RETAINER</b>\n"
        "────────────────────────────\n"
        "🔥 <b>Наше главное УТП — «Несгораемый результат»:</b>\n"
        "В обычных студиях вы платите абонентку «за воздух»: если бот не ломался, ваши деньги просто сгорают. "
        "У нас иначе: <b>если в течение месяца вы не ставили задач на тех. правки, наши маркетолог и аналитик сами "
        "проводят аудит вашей воронки, готовят прогревающую рассылку по базе и проверяют её по 152-ФЗ и ОРД!</b>\n\n"
        "────────────────────────────\n"
        "🛡 <b>1. Тариф [PXL // SLA BASE] — 5 900 ₽ / мес</b>\n"
        "<i>Для квизов и лид-ботов (по цене пустого конструктора, но всё делаем мы руками!)</i>\n"
        "• Размещение на защищенных серверах РФ (VPS) + мониторинг 24/7 + ежедневные бэкапы БД\n"
        "• <b>До 2 часов работы инженера в месяц</b> (замена цен, текстов, фото, кнопок по сообщению в ТГ)\n"
        "• Время реакции (SLA): до 4 часов\n\n"
        "🚀 <b>2. Тариф [PXL // GROWTH] — 12 900 ₽ / мес</b> <i>(Выбор 70% клиентов)</i>\n"
        "<i>Для активного бизнеса с трафиком и интеграциями</i>\n"
        "• Всё из тарифа SLA BASE + приоритетная реакция <b>до 1 часа</b> (включая выходные)\n"
        "• <b>До 5 часов работы команды в месяц</b> (доработка веток, интеграций с CRM, логики)\n"
        "• <b>+ 1 акционная/прогревающая рассылка в месяц по базе бота «под ключ»</b>\n"
        "• Юридическая проверка рассылок и маркировка рекламы (токены <code>erid</code> / ОРД / 152-ФЗ)\n\n"
        "💎 <b>3. Тариф [PXL // SCALE PRO] — 24 900 ₽ / мес</b>\n"
        "<i>Выделенный IT-отдел для Telegram Mini Apps и крупных проектов</i>\n"
        "• Выделенный сервер под высокую нагрузку (Stage + Prod) и реакция до 30 минут 24/7\n"
        "• <b>До 10 часов разработки (React/Python/UI)</b> на внедрение новых экранов и фич каждый месяц\n"
        "• До 3 рассылок в месяц, аналитика конверсии воронки с PM (MBA) и полный юр. щит\n\n"
        "🚑 <b>У вас уже есть бот от другого разработчика, но он упал или требует правок?</b>\n"
        "Нажмите кнопку ниже — мы проведем аудит и возьмем вашего бота на наш сервер и баланс!"
    )
    await call.message.edit_text(text=text, reply_markup=get_support_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "start_support_audit")
async def cb_start_support_audit(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(SupportAuditStates.entering_bot_link)
    text = (
        "🚑 <b>РЕАНИМАЦИЯ / ПЕРЕНОС СУЩЕСТВУЮЩЕГО БОТА НА ПОДДЕРЖКУ</b>\n"
        "────────────────────────────\n"
        "Разработчик пропал, отключился сервер, нужно обновить цены или перенести бота с конструктора?\n\n"
        "Напишите <b>ссылку/@username вашего бота</b> и кратко опишите, что сейчас не работает или что нужно доработать:"
    )
    await call.message.edit_text(text=text, reply_markup=get_cancel_kb(), parse_mode="HTML")
    await call.answer()

@router.message(SupportAuditStates.entering_bot_link)
async def process_support_bot_link(message: Message, state: FSMContext):
    await state.update_data(bot_info=message.text)
    await state.set_state(SupportAuditStates.entering_contact)
    text = (
        "👍 Принято! Теперь укажите ваше <b>Имя</b> и контакт для связи (Telegram @username или телефон), "
        "чтобы наш ведущий инженер провел экспресс-диагностику:"
    )
    await message.answer(text=text, reply_markup=get_cancel_kb(), parse_mode="HTML")

@router.message(SupportAuditStates.entering_contact)
async def process_support_contact(message: Message, state: FSMContext, bot: Bot):
    contact = message.text
    data = await state.get_data()
    bot_info = data.get("bot_info", "Не указано")
    await state.clear()

    await message.answer(
        "✅ <b>Заявка на диагностику и сопровождение принята!</b>\n"
        "────────────────────────────\n"
        "Мы проверим вашего бота и свяжемся с вами в ближайшее время с планом восстановления и запуска.",
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

    target_admin_id = get_admin_id()
    if target_admin_id and target_admin_id != 0:
        admin_text = (
            "🚑 <b>ЗАЯВКА НА ПОЧИНКУ / СОПРОВОЖДЕНИЕ ЧУЖОГО БОТА!</b>\n"
            "────────────────────────────\n"
            f"👤 <b>Контакты клиента:</b> {contact}\n"
            f"📱 <b>От пользователя:</b> @{message.from_user.username or 'не указан'} (ID: <code>{message.from_user.id}</code>)\n\n"
            f"🤖 <b>Бот и описание проблемы:</b>\n{bot_info}"
        )
        try:
            await bot.send_message(chat_id=target_admin_id, text=admin_text, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка отправки уведомления админу: {e}")

# ────────────────────────── РАЗДЕЛ ДЛЯ ИНВЕСТОРОВ (VENTURE BUILDER) ──────────────────────────

@router.callback_query(F.data == "venture_menu")
async def cb_venture_menu(call: CallbackQuery):
    text = (
        "📈 <b>PXLBOT VENTURES // ДЛЯ БИЗНЕС-АНГЕЛОВ И SMART MONEY</b>\n"
        "────────────────────────────\n"
        "Помимо клиентского продакшна, <b>PxlBot Studios</b> работает по модели <b>Venture Builder</b> — "
        "мы создаем собственные отраслевые платформы в формате Telegram Mini Apps и Web на рынках с высоким чеком.\n\n"
        "<b>Главное преимущество для инвестора:</b>\n"
        "Рабочие MVP наших платформ уже написаны в коде собственной инхаус-командой (Backend, Frontend, UI/UX, "
        "Legal ЕАПК, Marketing, PM MBA). Инвестиции идут напрямую в захват рынка и дистрибуцию.\n\n"
        "<b>Открыты к диалогу по 3 нашим продуктам:</b>\n"
        "1️⃣ <b>«Агротерминал»</b> — ценовой B2B-терминал зернового рынка РФ (котировки CPT/EXW, пошлины, калькулятор Netback «EXW Ангар»).\n"
        "2️⃣ <b>«Агротрейд»</b> — биржевой стакан прямых закупочных бидов от экспортеров и МЭЗов с фиксацией объема в 1 клик.\n"
        "3️⃣ <b>«ЮрБиржа»</b> — двухсторонний LegalTech-маркетплейс с безопасной сделкой (Escrow), проверкой дипломов через ФИС ФРДО и арбитражем за 48ч.\n\n"
        "👇 Изучите карточки платформ или напишите основателю для запроса live-демо и финмодели:"
    )
    await call.message.edit_text(text=text, reply_markup=get_venture_kb(), parse_mode="HTML")
    await call.answer()

# ────────────────────────── КАЛЬКУЛЯТОР СТОИМОСТИ ──────────────────────────

@router.callback_query(F.data == "start_calc")
async def cb_start_calc(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(CalculatorStates.choosing_product)
    text = (
        "🧮 <b>КАЛЬКУЛЯТОР ПРОЕКТА // ШАГ 1 ИЗ 3</b>\n"
        "────────────────────────────\n"
        "Какой формат задачи вам требуется решить?"
    )
    await call.message.edit_text(text=text, reply_markup=get_calc_product_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(CalculatorStates.choosing_product, F.data.startswith("calc_prod_"))
async def cb_calc_prod(call: CallbackQuery, state: FSMContext):
    prod_type = call.data.replace("calc_prod_", "")
    await state.update_data(product=prod_type)
    await state.set_state(CalculatorStates.choosing_niche)

    text = (
        "🧮 <b>КАЛЬКУЛЯТОР ПРОЕКТА // ШАГ 2 ИЗ 3</b>\n"
        "────────────────────────────\n"
        "В какой сфере работает ваш проект?"
    )
    await call.message.edit_text(text=text, reply_markup=get_calc_niche_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(CalculatorStates.choosing_niche, F.data.startswith("calc_niche_"))
async def cb_calc_niche(call: CallbackQuery, state: FSMContext):
    niche = call.data.replace("calc_niche_", "")
    await state.update_data(niche=niche)
    await state.set_state(CalculatorStates.choosing_integration)

    text = (
        "🧮 <b>КАЛЬКУЛЯТОР ПРОЕКТА // ШАГ 3 ИЗ 3</b>\n"
        "────────────────────────────\n"
        "Какой контур интеграций необходим?"
    )
    await call.message.edit_text(text=text, reply_markup=get_calc_integration_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(CalculatorStates.choosing_integration, F.data.startswith("calc_int_"))
async def cb_calc_int(call: CallbackQuery, state: FSMContext):
    integration = call.data.replace("calc_int_", "")
    data = await state.get_data()
    prod = data.get("product", "quizbot")

    # Рыночная сетка PxlBot Studios
    if prod == "quizbot":
        min_p, max_p = 25000, 35000
        days = "3–5 дней"
        prod_title = "Квиз-воронка / Лид-бот"
        rec_sla = "[PXL // SLA BASE] — 5 900 ₽/мес (сервер РФ 24/7 + бэкапы + до 2 ч правок)"
    elif prod == "bizbot":
        min_p, max_p = 50000, 70000
        days = "7–12 дней"
        prod_title = "Бизнес-бот с автоматизацией"
        rec_sla = "[PXL // GROWTH] — 12 900 ₽/мес (сервер + 5 ч команды + 1 рассылка/мес + 152-ФЗ/ОРД)"
    elif prod == "miniapp":
        min_p, max_p = 95000, 150000
        days = "14–25 дней"
        prod_title = "Telegram Mini App (WebApp)"
        rec_sla = "[PXL // SCALE PRO] — 24 900 ₽/мес (выделенный сервер + 10 ч React/Python + маркетинг и юр. щит)"
    else:  # reanimate
        min_p, max_p = 10000, 25000
        days = "1–3 дня"
        prod_title = "Реанимация / Доработка существующего бота"
        rec_sla = "[PXL // SLA BASE] — 5 900 ₽/мес (перенос на наш сервер + мониторинг 24/7 + 2 ч правок)"

    int_title = "Базовый контур (внутри Telegram)"
    if integration == "crm":
        min_p += 5000
        max_p += 8000
        int_title = "Интеграция с CRM / Google Таблицами"
    elif integration == "pay":
        min_p += 7000
        max_p += 10000
        int_title = "Онлайн-оплата (СБП / ЮKassa)"
    elif integration == "all":
        min_p += 12000
        max_p += 20000
        int_title = "Полный контур (CRM + Оплата + AI / Админка)"

    price_str = f"{min_p:,} – {max_p:,} ₽".replace(",", " ")

    await state.update_data(
        final_product=prod_title,
        final_int=int_title,
        price_range=price_str,
        days=days,
        rec_sla=rec_sla
    )

    text = (
        "📊 <b>ПРЕДВАРИТЕЛЬНЫЙ РАСЧЕТ ПРОЕКТА</b>\n"
        "────────────────────────────\n"
        f"• <b>Решение:</b> {prod_title}\n"
        f"• <b>Интеграции:</b> {int_title}\n"
        f"• <b>Ориентировочный бюджет:</b> <code>{price_str}</code>\n"
        f"• <b>Срок запуска:</b> {days}\n\n"
        "🎁 <b>Что уже включено в смету:</b>\n"
        "✅ Чистый код без абонентской платы конструкторам\n"
        "✅ Юридический базовый контур (согласие на ПДн по 152-ФЗ)\n"
        "✅ <b>Первые 14 дней сопровождения и сервера — БЕСПЛАТНО!</b>\n\n"
        f"🛡 <b>Рекомендуемое сопровождение с 15-го дня:</b>\n"
        f"<code>{rec_sla}</code>\n\n"
        "Нажмите кнопку ниже, чтобы зафиксировать расчет и получить детальное КП:"
    )

    await call.message.edit_text(text=text, reply_markup=get_calc_result_kb(), parse_mode="HTML")
    await call.answer()

@router.callback_query(F.data == "calc_submit_order")
async def cb_calc_submit(call: CallbackQuery, state: FSMContext):
    await state.set_state(CalculatorStates.entering_contact)
    text = (
        "✍️ <b>ОФОРМЛЕНИЕ ЗАЯВКИ НА РАСЧЕТ</b>\n"
        "────────────────────────────\n"
        "Напишите ваше <b>Имя</b> и удобный способ связи (Telegram @username или номер телефона).\n\n"
        "<i>Пример: Александр, @alex_owner, +7 999 123-45-67</i>"
    )
    await call.message.edit_text(text=text, reply_markup=get_cancel_kb(), parse_mode="HTML")
    await call.answer()

@router.message(CalculatorStates.entering_contact)
async def process_calc_contact(message: Message, state: FSMContext, bot: Bot):
    contact = message.text
    data = await state.get_data()
    await state.clear()

    await message.answer(
        "✅ <b>Заявка успешно принята!</b>\n"
        "────────────────────────────\n"
        "Руководитель студии (@Nicky_pxl) уже получил параметры вашего расчета "
        "и свяжется с вами в ближайшее время.",
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

    target_admin_id = get_admin_id()
    if target_admin_id and target_admin_id != 0:
        admin_text = (
            "🚨 <b>НОВАЯ ЗАЯВКА ИЗ КАЛЬКУЛЯТОРА!</b>\n"
            "────────────────────────────\n"
            f"👤 <b>Клиент:</b> {contact}\n"
            f"📱 <b>От пользователя:</b> @{message.from_user.username or 'не указан'} (ID: <code>{message.from_user.id}</code>)\n\n"
            f"📦 <b>Решение:</b> {data.get('final_product')}\n"
            f"🔌 <b>Интеграции:</b> {data.get('final_int')}\n"
            f"💰 <b>Расчетная смета:</b> {data.get('price_range')}\n"
            f"⏱ <b>Срок:</b> {data.get('days')}\n"
            f"🛡 <b>Рекомендованный SLA:</b> {data.get('rec_sla')}"
        )
        try:
            await bot.send_message(chat_id=target_admin_id, text=admin_text, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка отправки уведомления админу: {e}")

# ────────────────────────── ПРЯМАЯ ЗАЯВКА НА РАЗРАБОТКУ ──────────────────────────

@router.callback_query(F.data == "start_order")
async def cb_start_order(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await state.set_state(OrderStates.entering_details)
    text = (
        "📝 <b>ОСТАВИТЬ ЗАЯВКУ // PXLBOT STUDIOS</b>\n"
        "────────────────────────────\n"
        "Опишите в 1–2 предложениях вашу задачу: какая у вас сфера бизнеса и что нужно разработать или взять на сопровождение?"
    )
    await call.message.edit_text(text=text, reply_markup=get_cancel_kb(), parse_mode="HTML")
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
        "Основатель PxlBot Studios (@Nicky_pxl) свяжется с вами в ближайшее время.",
        reply_markup=get_main_menu_kb(),
        parse_mode="HTML"
    )

    target_admin_id = get_admin_id()
    if target_admin_id and target_admin_id != 0:
        admin_text = (
            "🔥 <b>ПРЯМАЯ ЗАЯВКА В PXLBOT STUDIOS!</b>\n"
            "────────────────────────────\n"
            f"👤 <b>Контакты:</b> {contact}\n"
            f"📱 <b>От пользователя:</b> @{message.from_user.username or 'не указан'} (ID: <code>{message.from_user.id}</code>)\n"
            f"📋 <b>Задача клиента:</b>\n{task}"
        )
        try:
            await bot.send_message(chat_id=target_admin_id, text=admin_text, parse_mode="HTML")
        except Exception as e:
            print(f"Ошибка отправки уведомления админу: {e}")
