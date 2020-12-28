import qrcode
import os
import fitz
from random import random

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Генерация QR-кода для поиска детали в базе
def qr_generator(code):
    # host = settings.ALLOWED_HOSTS[0]
    # detail_view_url = 'http://' + str(host) + '/all/Position/' + title

    detail_view_url = 'http://127.0.0.1:8000/position/view/' + code
    text = str(code)
    img = qrcode.make(detail_view_url)  # TODO: Тут ошибка! Сраный .NET
    img_path = os.path.join(BASE_DIR, 'media/POSITION_QR_CODE/') + text + '.png'

    try:
        img.save(img_path)
        # filename convert
        img_name = 'POSITION_QR_CODE/' + text + '.png'  # 'media/
        # print(img_path, '>', img_name)

    except Exception:
        print('Error save')

    return img_name


# Генерация QR-кода для операций производства
def qr_generator_production(code):
    # host = settings.ALLOWED_HOSTS[0]
    # detail_view_url = 'http://' + str(host) + '/all/Position/' + title
    detail_view_url = 'http://127.0.0.1:8000/position/production_view/' + code
    text = str(code)
    img = qrcode.make(detail_view_url)
    img_path = os.path.join(BASE_DIR, 'media/POSITION_QR_CODE_PRODUCTION/') + text + '.png'
    try:
        img.save(img_path)
        # filename convert
        img_name = 'POSITION_QR_CODE_PRODUCTION/' + text + '.png'  # 'media/
        #print(img_path, '>', img_name)

    except Exception:
        print('Error save')

    return img_name


# Проверка формата чертежа
def file_size_check(file):
    try:
        doc = fitz.open(file)
    except:
        print(file)
        print('Ошибка чтения файла')

    page = doc[0]
    long = page.MediaBox[2]
    height = page.MediaBox[3]
    if 550 < long < 700:
        if 800 < height < 900:
            return "A4"
    elif 1150 < long < 1250:
        if 800 < height < 900:
            return "A3"
    elif 1600 < long < 1750:
        if 1100 < height < 1300:
            return "A2"
    else:
        return "A4"


# Подготовка к модификации PDF-чертежа
def create_modify_draw(component, position, order):
    try:
        # Получение формата pdf чертежа
        pdf_path = component.draw_pdf.path
        a = random()
        b = a * 10000000000000
        c = str(b)[:13]

        component_pdf_size = file_size_check(pdf_path)

        # Получение пути к модицицированному черетжу с qr кодом
        sticker_draw_pdf_path = 'POSITION_DRAW_PDF/' + c + '.PDF'

        # Создание модифицированного pdf чертежа с qr кодом
        sticker_draw_pdf = create_work_pdf(component.draw_pdf, sticker_draw_pdf_path, position.qr_code_production,
                                           order.project.title, order.title, position.mather_assembly,
                                           position.quantity, component_pdf_size)
        return True
    except Exception:
        return False


# Создание модифицированного рабочего чертежа
def create_work_pdf(old_pdf_file, new_pdf_file, qr_code_path, project_name, order_name, mather_assembly_name, quantity,
                    file_size):
    print("Выполняется создание рабочаего чертежа")

    real_old_pdf_file = os.path.join(BASE_DIR, 'media/') + str(old_pdf_file)
    real_old_pdf_file = real_old_pdf_file.replace('\\', '/')
    real_new_pdf_file = os.path.join(BASE_DIR, 'media/') + str(new_pdf_file)
    real_new_pdf_file = real_new_pdf_file.replace('\\', '/')
    real_qr_code_path = os.path.join(BASE_DIR, 'media/') + str(qr_code_path)
    real_qr_code_path = real_qr_code_path.replace('\\', '/')
    doc = fitz.open(real_old_pdf_file)

    mstb = 1.378
    print(file_size)
    if file_size == "A4":
        qr_rect = fitz.Rect(666 / mstb, 1000 / mstb, (666 + 64) / mstb, (1000 + 64) / mstb)
        project_rect = fitz.Rect(609 / mstb, 1082 / mstb, (609 + 200) / mstb, (1082 + 16) / mstb)
        order_rect = fitz.Rect(609 / mstb, 1097 / mstb, (609 + 200) / mstb, (1097 + 16) / mstb)
        mather_assembly_rect = fitz.Rect(609 / mstb, 1111 / mstb, (609 + 200) / mstb, (1111 + 16) / mstb)
        quantity_rect = fitz.Rect(609 / mstb, 1126 / mstb, (609 + 200) / mstb, (1126 + 16) / mstb)
    elif file_size == 'A3':
        i = 595 * mstb
        qr_rect = fitz.Rect((666 + i) / mstb, 1000 / mstb, ((666 + i) + 64) / mstb, (1000 + 64) / mstb)
        project_rect = fitz.Rect((609 + i) / mstb, 1082 / mstb, ((609 + i) + 200) / mstb, (1082 + 16) / mstb)
        order_rect = fitz.Rect((609 + i) / mstb, 1097 / mstb, ((609 + i) + 200) / mstb, (1097 + 16) / mstb)
        mather_assembly_rect = fitz.Rect((609 + i) / mstb, 1111 / mstb, ((609 + i) + 200) / mstb, (1111 + 16) / mstb)
        quantity_rect = fitz.Rect((609 + i) / mstb, 1126 / mstb, ((609 + i) + 200) / mstb, (1126 + 16) / mstb)
    elif file_size == 'A2':
        i = 1089 * mstb
        j = 348 * mstb
        qr_rect = fitz.Rect((666 + i) / mstb, (1000 + j) / mstb, ((666 + i) + 64) / mstb, ((1000 + j) + 64) / mstb)
        project_rect = fitz.Rect((609 + i) / mstb, (1082 + j) / mstb, ((609 + i) + 200) / mstb,
                                 ((1082 + j) + 16) / mstb)
        order_rect = fitz.Rect((609 + i) / mstb, (1097 + j) / mstb, ((609 + i) + 200) / mstb, ((1097 + j) + 16) / mstb)
        mather_assembly_rect = fitz.Rect((609 + i) / mstb, (1111 + j) / mstb, ((609 + i) + 200) / mstb,
                                         ((1111 + j) + 16) / mstb)
        quantity_rect = fitz.Rect((609 + i) / mstb, (1126 + j) / mstb, ((609 + i) + 200) / mstb,
                                  ((1126 + j) + 16) / mstb)

    project_text = "Проект: " + project_name
    order_text = "Заказ: " + order_name
    assembly_text = "Сборка: " + mather_assembly_name
    quantity_text = "Кол-во: " + str(quantity)

    page = doc[0]
    page.insertImage(qr_rect, filename=real_qr_code_path)

    font_path = os.path.join(BASE_DIR, 'static/admin/fonts/9807.ttf')
    print("Путь к файлу шрифта: " + font_path)

    rc1 = page.insertTextbox(project_rect, project_text, fontsize=9,
                             fontname="FreeSans",  # a PDF standard font
                             fontfile=font_path,
                             # could be a file on your system
                             align=0)
    rc2 = page.insertTextbox(order_rect, order_text, fontsize=9,
                             fontname="FreeSans",  # a PDF standard font
                             fontfile=font_path,
                             # could be a file on your system
                             align=0)
    rc3 = page.insertTextbox(mather_assembly_rect, assembly_text, fontsize=9,
                             fontname="FreeSans",  # a PDF standard font
                             fontfile=font_path,
                             # could be a file on your system
                             align=0)
    rc4 = page.insertTextbox(quantity_rect, quantity_text, fontsize=9,
                             fontname="FreeSans",  # a PDF standard font
                             fontfile=font_path,
                             # could be a file on your system
                             align=0)

    doc.save(real_new_pdf_file)
    print("Рабочий чертеж создан!")

    return new_pdf_file
