# -*- coding: utf-8 -*-
"""
PxlBot Studios // Генератор официальных смет (Приложение №1 к Договору)
Форматирование строго по стандартам B2B:
- Шрифт: Times New Roman
- Выравнивание основного текста: по ширине (Justified)
- Абзацный отступ (красная строка): 1.25 см
- Блок "Приложение № 1": по левому краю
- Таблица сметы с четкими границами и разбивкой по этапам
- Логотип PxlBot Studios в шапке документа
"""

import os
import datetime
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement
from docx.oxml.ns import qn


def _set_cell_background(cell, hex_color: str):
    """Установка фонового цвета ячейки таблицы"""
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tc_pr.append(shd)


def _set_cell_margins(cell, top=120, bottom=120, left=150, right=150):
    """Установка внутренних отступов ячейки таблицы (в dxa, 20 dxa = 1 pt)"""
    tc_pr = cell._tc.get_or_add_tcPr()
    tc_mar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tc_mar.append(node)
    tc_pr.append(tc_mar)


def _set_table_borders(table, color='B0B0B0', sz='4'):
    """Установка тонких аккуратных границ таблицы"""
    tbl_pr = table._tbl.tblPr
    tbl_borders = OxmlElement('w:tblBorders')
    for b_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        b = OxmlElement(f'w:{b_name}')
        b.set(qn('w:val'), 'single')
        b.set(qn('w:sz'), sz)
        b.set(qn('w:space'), '0')
        b.set(qn('w:color'), color)
        tbl_borders.append(b)
    tbl_pr.append(tbl_borders)


def _apply_run_font(run, font_name="Times New Roman", size_pt=12, bold=False, italic=False, color_rgb=(0, 0, 0)):
    """Применение шрифта Times New Roman и параметров к конкретному run"""
    run.font.name = font_name
    run.font.size = Pt(size_pt)
    run.bold = bold
    run.italic = italic
    run.font.color.rgb = RGBColor(*color_rgb)
    # Принудительная установка шрифта в w:rFonts для корректного отображения кириллицы в Word
    r_pr = run._r.get_or_add_rPr()
    r_fonts = OxmlElement('w:rFonts')
    r_fonts.set(qn('w:ascii'), font_name)
    r_fonts.set(qn('w:hAnsi'), font_name)
    r_fonts.set(qn('w:cs'), font_name)
    r_fonts.set(qn('w:eastAsia'), font_name)
    r_pr.append(r_fonts)


def _add_justified_paragraph(doc, text="", bold_prefix="", space_after=4, first_line_indent=1.25):
    """Добавление абзаца с выравниванием по ширине и красной строкой 1.25 см"""
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.line_spacing = 1.15
    p.paragraph_format.space_after = Pt(space_after)
    if first_line_indent > 0:
        p.paragraph_format.first_line_indent = Cm(first_line_indent)
    else:
        p.paragraph_format.first_line_indent = Cm(0)

    if bold_prefix:
        r_pre = p.add_run(bold_prefix)
        _apply_run_font(r_pre, bold=True)
    if text:
        r_text = p.add_run(text)
        _apply_run_font(r_text)
    return p


def generate_smeta_docx(data: dict, client_contact: str = "", output_path: str = None) -> str:
    """
    Генерирует официальный Word-документ (.docx) Сметы и ТЗ (Приложение №1).
    Возвращает путь к сгенерированному файлу.
    """
    doc = docx.Document()

    # Настройка полей страницы (2 см со всех сторон)
    for section in doc.sections:
        section.top_margin = Cm(2.0)
        section.bottom_margin = Cm(2.0)
        section.left_margin = Cm(2.5)
        section.right_margin = Cm(1.5)

    # 1. Поиск логотипа PxlBot Studios
    possible_logo_paths = [
        r'C:\Users\Валера куплю гараж\Desktop\PxlBot Studios\Айдентика\Логотип PxlBot PNG.png',
        r'C:\Users\Валера куплю гараж\Desktop\PxlBot Studios\Айдентика\Логотип PxlBot.png',
        r'C:\Users\Валера куплю гараж\Desktop\PxlBot Studios\Айдентика\Логотип-PxlBot.jpg',
        os.path.join(os.path.dirname(__file__), 'logo.png')
    ]
    logo_found = None
    for lp in possible_logo_paths:
        if os.path.exists(lp):
            logo_found = lp
            break

    # Шапка с логотипом
    if logo_found:
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_logo.paragraph_format.space_after = Pt(6)
        p_logo.paragraph_format.first_line_indent = Cm(0)
        run_logo = p_logo.add_run()
        run_logo.add_picture(logo_found, width=Inches(1.5))

    # 2. Блок "Приложение № 1" (строго по левому краю по требованию)
    p_app = doc.add_paragraph()
    p_app.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_app.paragraph_format.first_line_indent = Cm(0)
    p_app.paragraph_format.line_spacing = 1.15
    p_app.paragraph_format.space_after = Pt(12)

    r_app1 = p_app.add_run("Приложение № 1\n")
    _apply_run_font(r_app1, bold=True, size_pt=11)
    r_app2 = p_app.add_run(
        "к Договору разработки программного обеспечения\n"
        "№ ____ от «___» ____________ 2026 г.\n"
    )
    _apply_run_font(r_app2, italic=True, size_pt=10, color_rgb=(80, 80, 80))

    # 3. Заголовок документа (по центру, 14 pt, Bold)
    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.first_line_indent = Cm(0)
    p_title.paragraph_format.space_before = Pt(6)
    p_title.paragraph_format.space_after = Pt(4)
    r_title = p_title.add_run("ТЕХНИЧЕСКОЕ ЗАДАНИЕ И КАЛЬКУЛЯЦИЯ СТОИМОСТИ РАБОТ\n(СМЕТА ПРОЕКТА)")
    _apply_run_font(r_title, size_pt=13, bold=True)

    # Город и дата
    now = datetime.datetime.now()
    months = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]
    date_str = f"«{now.day:02d}» {months[now.month - 1]} {now.year} г."

    p_city_date = doc.add_paragraph()
    p_city_date.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_city_date.paragraph_format.first_line_indent = Cm(0)
    p_city_date.paragraph_format.space_after = Pt(14)
    r_cd_left = p_city_date.add_run("г. Екатеринбург")
    _apply_run_font(r_cd_left, bold=True, size_pt=11)
    # Табуляция вправо для даты
    r_cd_spaces = p_city_date.add_run("\t\t\t\t\t\t\t\t\t\t" + date_str)
    _apply_run_font(r_cd_spaces, italic=True, size_pt=11)

    # Извлечение параметров сметы
    product_title = data.get("final_product", "Telegram Mini App (WebApp)")
    prod_price_str = data.get("final_prod_price", "85 000 ₽")
    niche_title = data.get("final_niche", "E-commerce / Селлеры")
    int_title = data.get("final_int", "Базовый контур (уведомления в Telegram)")
    int_price_str = data.get("final_int_price", "0 ₽")
    addon_title = data.get("final_addon", "Без доп. модулей")
    addon_price_str = data.get("final_addon_price", "0 ₽")
    total_price_str = data.get("price_total", "85 000 ₽")
    days_str = data.get("days", "15–20 рабочих дней")
    rec_support = data.get("rec_support", "Тариф «Базовый» — 5 900 ₽/мес")

    # Предоплата 50%
    try:
        total_int = int(''.join(filter(str.isdigit, total_price_str)))
        advance_50 = f"{total_int // 2:,} ₽".replace(",", " ")
        final_50 = f"{(total_int - total_int // 2):,} ₽".replace(",", " ")
    except Exception:
        advance_50 = "50% от общей суммы"
        final_50 = "50% от общей суммы"

    # 4. Раздел 1: Предмет разработки
    _add_justified_paragraph(doc, "", bold_prefix="1. Предмет разработки и параметры программного комплекса", space_after=6, first_line_indent=0)
    
    client_info = client_contact if client_contact else "Уточняется при заключении Договора"
    _add_justified_paragraph(
        doc,
        f"Исполнитель обязуется выполнить комплексную разработку, конфигурацию и внедрение программного обеспечения "
        f"типа «{product_title}» для автоматизации бизнес-процессов Заказчика в сегменте «{niche_title}». "
        f"Заказчик обязуется принять результат надлежащим образом выполненных работ и оплатить их стоимость в соответствии с настоящей Сметой.",
        bold_prefix="1.1. "
    )
    _add_justified_paragraph(
        doc,
        f"Заказчик (контактное лицо): {client_info}. Исполнитель: Студия заказной разработки «PxlBot Studios» "
        f"(Руководитель проекта / основатель: @Nicky_pxl).",
        bold_prefix="1.2. Стороны проекта: "
    )

    # 5. Раздел 2: Таблица сметы
    _add_justified_paragraph(doc, "", bold_prefix="2. Калькуляция стоимости и функциональный состав этапов работ", space_after=6, first_line_indent=0)

    # Создание таблицы
    table = doc.add_table(rows=1, cols=5)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    _set_table_borders(table)

    # Шапка таблицы
    headers = [
        ("№", Inches(0.4)),
        ("Наименование модуля / этапа", Inches(1.8)),
        ("Техническое описание и состав реализуемых работ", Inches(2.9)),
        ("Срок", Inches(0.8)),
        ("Стоимость", Inches(1.1))
    ]

    hdr_cells = table.rows[0].cells
    for i, (title, width) in enumerate(headers):
        hdr_cells[i].width = width
        p_cell = hdr_cells[i].paragraphs[0]
        p_cell.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cell.paragraph_format.first_line_indent = Cm(0)
        p_cell.paragraph_format.space_after = Pt(2)
        r = p_cell.add_run(title)
        _apply_run_font(r, size_pt=10, bold=True)
        _set_cell_background(hdr_cells[i], "EAECEF")
        _set_cell_margins(hdr_cells[i], top=100, bottom=100, left=100, right=100)

    # Строки этапов
    rows_data = [
        (
            "1",
            f"Программное ядро и интерфейс:\n{product_title}",
            "Проектирование системной архитектуры, верстка UI-экранов, FSM-маршрутизация диалогов, "
            "валидация пользовательского ввода, настройка асинхронного обработчика событий и системного меню.",
            days_str.split(" ")[0],
            prod_price_str
        ),
        (
            "2",
            f"Отраслевой контур:\n{niche_title}",
            "Развертывание реляционной базы данных (SQLite/PostgreSQL), реализация товарных/услуговых матриц, "
            "калькуляторов стоимости, модуля квалификации лидов и отправки карточки заказа в панель администратора.",
            "Включено",
            "Включено в ядро"
        ),
        (
            "3",
            f"Интеграционный шлюз:\n{int_title}",
            "Настройка защищенных REST API вебхуков, связка с внешней CRM-системой (AmoCRM / Bitrix24) "
            "и/или платежным шлюзом (СБП, эквайринг, чеки) для фискализации и автоматической фиксации сделок.",
            "2–3 раб. дня",
            int_price_str
        ),
        (
            "4",
            f"Дополнительные модули:\n{addon_title}",
            "Подключение расширенных сценариев (AI-ассистент на базе LLM, рассылочный комбайн, "
            "программа лояльности или расширенное регламентное сопровождение запуска).",
            "1–2 раб. дня",
            addon_price_str
        )
    ]

    for r_idx, row in enumerate(rows_data, 1):
        row_cells = table.add_row().cells
        for c_idx, val in enumerate(row):
            p_c = row_cells[c_idx].paragraphs[0]
            p_c.paragraph_format.first_line_indent = Cm(0)
            p_c.paragraph_format.space_after = Pt(2)
            if c_idx in [0, 3, 4]:
                p_c.alignment = WD_ALIGN_PARAGRAPH.CENTER
            else:
                p_c.alignment = WD_ALIGN_PARAGRAPH.LEFT
            r = p_c.add_run(val)
            _apply_run_font(r, size_pt=9.5)
            _set_cell_margins(row_cells[c_idx], top=80, bottom=80, left=100, right=100)
            if r_idx % 2 == 0:
                _set_cell_background(row_cells[c_idx], "F8F9FA")

    # Итоговая строка
    total_row = table.add_row().cells
    total_row[0].merge(total_row[3])
    p_tot_lbl = total_row[0].paragraphs[0]
    p_tot_lbl.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_tot_lbl.paragraph_format.first_line_indent = Cm(0)
    r_tot_lbl = p_tot_lbl.add_run("ИТОГО ПО НАСТОЯЩЕЙ СМЕТЕ:")
    _apply_run_font(r_tot_lbl, size_pt=10, bold=True)
    _set_cell_background(total_row[0], "EAECEF")
    _set_cell_margins(total_row[0], top=100, bottom=100, left=100, right=100)

    p_tot_val = total_row[4].paragraphs[0]
    p_tot_val.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_tot_val.paragraph_format.first_line_indent = Cm(0)
    r_tot_val = p_tot_val.add_run(total_price_str)
    _apply_run_font(r_tot_val, size_pt=10.5, bold=True, color_rgb=(10, 80, 30))
    _set_cell_background(total_row[4], "E2EFDA")
    _set_cell_margins(total_row[4], top=100, bottom=100, left=100, right=100)

    p_vat = doc.add_paragraph()
    p_vat.paragraph_format.first_line_indent = Cm(0)
    p_vat.paragraph_format.space_before = Pt(4)
    p_vat.paragraph_format.space_after = Pt(10)
    r_vat = p_vat.add_run("*НДС не облагается в связи с применением специального налогового режима (ст. 346.11 / гл. 26.2 НК РФ).")
    _apply_run_font(r_vat, italic=True, size_pt=9, color_rgb=(100, 100, 100))

    # 6. Раздел 3: Порядок оплаты и график сдачи
    _add_justified_paragraph(doc, "", bold_prefix="3. Порядок оплаты и условия сдачи-приемки работ", space_after=6, first_line_indent=0)
    _add_justified_paragraph(
        doc,
        f"Оплата работ производится в два этапа: Авансовый платеж в размере 50% ({advance_50}) выплачивается "
        f"Заказчиком в течение 3 (трех) банковских дней с даты подписания настоящего Приложения. Окончательный расчет "
        f"в размере 50% ({final_50}) производится в течение 3 (трех) банковских дней после подписания Акта сдачи-приемки выполненных работ.",
        bold_prefix="3.1. График платежей: "
    )
    _add_justified_paragraph(
        doc,
        f"Общий нормативный срок разработки составляет {days_str} с даты внесения авансового платежа и "
        f"предоставления Заказчиком базовых текстово-графических исходных материалов.",
        bold_prefix="3.2. Сроки выполнения: "
    )
    _add_justified_paragraph(
        doc,
        "Заказчик обязуется в течение 3 (трех) рабочих дней с момента получения уведомления о готовности и "
        "ссылки на программный комплекс произвести проверку работоспособности и подписать Акт сдачи-приемки "
        "либо направить мотивированный письменный отказ с перечнем замечаний, не выходящих за рамки настоящей Сметы. "
        "В случае непредставления мотивированного отказа в указанный 3-дневный срок, работы признаются выполненными "
        "в полном объеме, надлежащего качества и принятыми Заказчиком в одностороннем порядке.",
        bold_prefix="3.3. Регламент приемки (Авто-акцепт): "
    )

    # 7. Раздел 4: Гарантийные обязательства
    _add_justified_paragraph(doc, "", bold_prefix="4. Гарантийные обязательства и сопровождение", space_after=6, first_line_indent=0)
    _add_justified_paragraph(
        doc,
        f"Исполнитель предоставляет безусловную гарантию на разработанный программный код сроком 15 (пятнадцать) "
        f"календарных дней со дня сдачи проекта. Любые критические дефекты, ошибки логики или сбои, возникшие по вине Исполнителя, "
        f"устраняются безвозмездно в приоритетном порядке. Дальнейшее регулярное обслуживание, масштабирование серверов и "
        f"маркетинговые рассылки осуществляются в рамках соглашения SLA ({rec_support}).",
        bold_prefix="4.1. Гарантийный регламент: "
    )

    # 8. Раздел 5: Подписи и печати Сторон
    _add_justified_paragraph(doc, "", bold_prefix="5. Адреса, реквизиты и подписи Сторон", space_after=8, first_line_indent=0)

    sig_table = doc.add_table(rows=1, cols=2)
    sig_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    sig_cells = sig_table.rows[0].cells
    sig_cells[0].width = Inches(3.5)
    sig_cells[1].width = Inches(3.5)

    # Исполнитель
    p_dev = sig_cells[0].paragraphs[0]
    p_dev.paragraph_format.first_line_indent = Cm(0)
    p_dev.paragraph_format.line_spacing = 1.15
    p_dev.paragraph_format.space_after = Pt(2)
    r_dev_hdr = p_dev.add_run("ОТ ИСПОЛНИТЕЛЯ:\n")
    _apply_run_font(r_dev_hdr, bold=True, size_pt=10.5)
    r_dev_body = p_dev.add_run(
        "PxlBot Studios\n"
        "Студия автономных ботов и Mini Apps\n"
        "Telegram: @Nicky_pxl\n"
        "Сайт: t.me/pxlbot_studios\n\n\n"
        "_____________________ / Никита В. /\n"
        "М.П."
    )
    _apply_run_font(r_dev_body, size_pt=9.5)

    # Заказчик
    p_cl = sig_cells[1].paragraphs[0]
    p_cl.paragraph_format.first_line_indent = Cm(0)
    p_cl.paragraph_format.line_spacing = 1.15
    p_cl.paragraph_format.space_after = Pt(2)
    r_cl_hdr = p_cl.add_run("ОТ ЗАКАЗЧИКА:\n")
    _apply_run_font(r_cl_hdr, bold=True, size_pt=10.5)
    r_cl_body = p_cl.add_run(
        f"{client_info}\n"
        f"Направление: {niche_title}\n\n\n\n\n"
        "_____________________ / _________________ /\n"
        "М.П."
    )
    _apply_run_font(r_cl_body, size_pt=9.5)

    # Сохранение документа
    if not output_path:
        ts = now.strftime("%Y%m%d_%H%M%S")
        safe_client = "".join(c for c in client_contact if c.isalnum() or c in "_-")[:15] or "Client"
        filename = f"Смета_PxlBot_Приложение_1_{safe_client}_{ts}.docx"
        
        # Проверяем наличие папки Desktop (для Windows) или используем локальную папку/tmp (для Bothost Linux)
        desktop_dir = os.path.join(os.path.expanduser("~"), "Desktop")
        if os.path.exists(desktop_dir):
            output_dir = desktop_dir
        else:
            output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generated_smetas")
            os.makedirs(output_dir, exist_ok=True)
            
        output_path = os.path.join(output_dir, filename)

    parent_dir = os.path.dirname(output_path)
    if parent_dir and not os.path.exists(parent_dir):
        os.makedirs(parent_dir, exist_ok=True)

    doc.save(output_path)
    return output_path


if __name__ == "__main__":
    # Тестовый прогон для верификации
    test_data = {
        "final_product": "Telegram Mini App (WebApp)",
        "final_prod_price": "85 000 ₽",
        "final_niche": "E-commerce / Селлеры WB & Ozon",
        "final_int": "Полный контур (CRM + Оплата + чеки)",
        "final_int_price": "18 000 ₽",
        "final_addon": "3 мес. техподдержки и рассылок под ключ",
        "final_addon_price": "19 000 ₽",
        "price_total": "122 000 ₽",
        "days": "20–25 рабочих дней",
        "rec_support": "Тариф «Выделенный IT-отдел» — 24 900 ₽/мес"
    }
    res = generate_smeta_docx(test_data, client_contact="Олег (@oleg_porsh, +7 999 123-45-67)")
    print(f"Смета успешно сгенерирована: {res}")
