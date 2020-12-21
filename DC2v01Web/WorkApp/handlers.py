import qrcode
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Генерация QR-кода для поиска детали в базе
def qr_generator(code):
    # host = settings.ALLOWED_HOSTS[0]
    # detail_view_url = 'http://' + str(host) + '/all/Position/' + title

    detail_view_url = 'http://127.0.0.1:8000/position/view/' + code
    text = str(code)
    img = qrcode.make(detail_view_url)  # TODO: Тут ошибка! Сраный C++
    img_path = os.path.join(BASE_DIR, 'media/POSITION_QR_CODE/') + text + '.png'

    try:
        img.save(img_path)
        # filename convert
        img_name = 'POSITION_QR_CODE/' + text + '.png' #'media/
        print(img_path, '>', img_name)

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
        print(img_path, '>', img_name)

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
