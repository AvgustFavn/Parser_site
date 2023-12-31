import os
import re
import shutil
import tempfile
import time
from io import BytesIO
from random import randint

import pandas as pd
import xlrd
from PIL import Image
import requests
from openpyxl.reader.excel import load_workbook
from openpyxl.utils.dataframe import dataframe_to_rows
from openpyxl.workbook import Workbook

from cat.valids import price_validator
from catalog.settings import BASE_DIR

common_words = {
    'размеры': ['размеры', 'измерения', 'вес', 'высота', 'ширина', 'глубина', 'длина'],
    'материал': ['состав', 'ткань', 'материал', 'текстиль', 'содержание', 'компоненты', 'элементы'],
    'цвет': ['цвет', 'расцветка', 'оттенок'],
    'Страна производства': ['страна', 'страна', 'страны производства'],
    'Производитель': ['производитель', 'изготовитель', 'поставщик'],
    'дисплей': ['экран', 'дисплей'],
    'мощность': ['мощность', ],
    'напряжение': ['напряжение', ],
    'Комплектация': ['комплектация', 'комплекте', 'набор'],
    'программы': ['программа', 'программы', 'функция', 'функции'],
    'Класс энергопотребления': ['класс энергопотребления', 'энергопотребление', 'класс энергоэффективности',
                                'энергоэффективности', "энергоэффективность"],
    'конфорки': ['конфорки', 'конфорок', 'конфорка'],
    'объем': ['объем', 'габариты', 'величина', 'размер'],
    'температура': ['максимальная температура', 'температура', 'минимальная температура'],
    'гриль': ['грилль', 'гриль'],
    'антипригарное покрытие': ['антипригарное покрытие', 'пригарает', 'антипригарка'],
    'уровень шума': ['уровень шума', 'шум', 'шумы'],
    'тип сушки': ['тип сушки', 'вид сушки', 'метод сушки', 'технология сушки', 'режим сушки', 'высушивание'],
    'хладагент': ['хладагент', 'хладогент', 'охладитель', 'хладоноситель', 'фреон'],
    'кол-во полок': ['кол-во полок', 'количествово полок', 'полки', 'полок'],
    'потребление воды': ['потребление воды', 'расход воды', 'использование воды', 'водопотребление'],
    'тип нагревательного элемента': ['тип нагревательного элемента', 'нагревательный элемент', 'нагреватель',
                                     'термоэлемент', 'нагревательная спираль'],
    'рабочая поверхность': ['рабочая зона', 'рабочая поверхность', 'поверхность'],
    'количество отделений': ['количество отделений', 'отделений', 'отделения'],
    'автоотключение': ['автоотключение', 'автоматическое отключение', 'автоматическое выключение',
                       'автоматическая остановка'],
    'степень обжарки': ['степень обжарки', 'степени обжарки'],
    'трафарет': ['трафарет', 'трафаретов', 'трафареты'],
    'регулировка термостата': ['регулировка термостата', 'термостат', 'регулировка температуры'],
    'автослив масла': ['автослив масла', 'автослив', 'автоматического слива', 'дренаж масла', 'автоматический сливной',
                       'автоматический отвод'],
    'поддержание температуры': ['поддержание температуры', 'поддержка температуры', 'контроль температуры',
                                'поддержание заданной температуры', 'термоконтроль'],
    'лимит веса': ['лимит веса', 'ограничение веса', 'максимальный вес', 'допустимый вес', 'допустимая масса',
                   'грузовой предел', 'грузоподъемност', 'максимальный вес для'],
    'точность взвешивания': ['точность взвешивания', 'точность измерения', 'точность весов'],
    'тип батареи': ['тип батареи', 'тип аккумулятора', 'тип питания'],
    'резюрвар для воды': ['резюрвар для воды', 'резервуар для хранения вод', 'водный резервуар', 'бак для воды',
                          'емкость для воды'],
    'скорость вращения': ['скорость вращения', 'скорость оборота', 'скорость кручения', 'максимальная скорость'],
    'автоотчистка': ['автоотчистка', 'автоматическая очистка', 'автоматической чистки', 'автоматическая система чистки',
                     'самоочистка'],
    'тип уборки': ['тип уборки', 'метод уборки', 'способ уборки', 'вид уборки', 'режим уборки', 'режимы уборки'],
    'регулятор мощности': ['регулятор мощности', 'контроллер мощност', 'управление мощностью'],
    'тип сенсоров': ['тип сенсоров', 'вид сенсоров'],
    'время работы': ['время работы', 'продолжительность работы', 'длительность работы', 'время функционирования',
                     'время работы без перерывов'],
    'время зарядки': ['продолжительность зарядки', 'время зарядки', 'время полной зарядки'],
    'способ крепления': ['способ крепления', 'метод крепления', 'вид крепления', 'способ закрепления', 'креплени'],
    'максимальное давление воды': ['максимальное давление воды', 'предел давления воды', 'максимальное гидравлическое',
                                   'водяное давление', 'максимальное внутреннее давление'],
    'максимальная производительность': ['макс производительность', 'макс. производительность',
                                        'максимальный уровень производительности', 'уровень производительности'],
    'регулировка газа': ['регулировка газа', 'управление подачей газа', 'регулирование потока газа',
                         'регулировка расхода газа', 'управление расходом газа', 'регулировка интенсивности газа',
                         'регулирование давления газа'],
    'форма корпуса': ['форма корпуса', 'конструкция корпуса', 'дизайн корпуса', 'геометрическая форма'],
    'тип топлива': ['тип топлива', 'вип топлива', 'сорт топлива', 'источник топлива'],
    'расход топлива': ['расход топлива', 'потребление топлива', 'расход использования топлива', 'количество топлива',
                       'энергопотребление топлива'],
    'мощность охлаждения': ['мощность охлаждения', 'охлаждающая способность', 'эффективность охлаждения',
                            'скорость охлаждения'],
    'мощность обогрева': ['мощность обогрева', 'тепловая мощность', 'уровень обогрева', 'скорость обогрева'],
    'отапливаемая территория': ['отапливаемая территория', 'Зона обогрева', 'Площадь отопления'],
    'тип челнока': ['тип челнока', 'вид челнока', 'разновидность челнок', 'челнок'],
    'регулировка скорости шитья': ['регулировка скорости шитья', 'скорости шитья', 'скорость шитья',
                                   'контроль скорости', 'регулировка скорости'],
    'двойная игла': ['двойная игла', 'двойной иглы', 'две иглы', 'параллельная игла', 'двойной шовная',
                     'двойной швейный', 'двойной стежок', 'двойная нить'],
    'защита от перегрева': ['защита от перегрева', 'защита от темп', 'контроля температур', 'контроль температур',
                            'термическая защита'],
    'насадки': ['насадки', 'насадк', 'адаптер'],
    'время для нагрева': ['время для нагрева', 'время нагрева', 'скорость нагрева'],
    'cамозатачивающиеся ножи': ['самозатачивающиеся ножи', 'самозатачивающиеся', 'автоматически затачивающиеся',
                                'затачивающ', 'автозатач'],
    'материал лезвий': ['материал лезвий', 'лезвия из', 'лезвие из', 'лезвие состоит'],
    'общее число мегапикселей матрицы': ['общее число мегапикселей матрицы', 'разрешение матрицы',
                                         'матрицы в мегапикселях', 'пикселей на матрице', ],
    'число эффективных мегапикселей': ['число эффективных мегапикселей', 'эффективных мегапикселей',
                                       'эффективные мегапиксели', ],
    'тип матрицы': ['тип матрицы', 'вид матрицы', 'разновидность матрицы'],
    'кроп фактор': ['кроп фактор', 'фактор кадрирования', 'коэффициент обрезки', 'кроп-фактор'],
    'максимальное разрешение': ['максимальное разрешение', 'наибольшее разрешение', 'максимальное число пикселей',
                                'максимальное количество пикселей', 'максимальное число точек'],
    'количество объективов': ['количество объективов', 'кол-во объективов', 'объективы', 'дополнительный объектив',
                              'дополнительные объективы'],
    'фокусное расстояние': ['фокусное расстояние', 'расстояние до фокуса', 'оптическое фокусное', 'фокусное'],
    'значение диафрагмы': ['значение диафрагмы', 'диафрагмальное отверстие', 'бленда', 'диафрагмальный затвор',
                           'регулятор диафрагмы'],
    'выдержка': ['выдержка', 'скорость затвора', 'время экспозиции', 'затворная скорость', 'время выдержки',
                 'длительность экспозиции'],
    'форматы фотографий': ['форматы фотографий', 'поддерживающие форматы', 'форматы изображений', 'форматы'],
    'поддержка 4К': ['поддержка 4К', 'поддержка 2160p', 'воспроизведение 4K-видео', 'поддержка 4K-разрешения',
                     '4K-совместимость'],
    'поддержка full hd': ['поддержка full hd', 'поддержка 1080p', 'воспроизведение full hd',
                          'поддержка full hd разрешения', 'full hd совместимость'],
    'процессор': ['процессор', 'cpu', 'центральный процессор', 'микропроцессор', 'ЦПУ'],
    'угол обзора': ['угол обзора', 'угол зрения', 'угол видимости', 'угол наблюдения', 'угол поля зрения'],
    'стабилизация картинки': ['стабилизация картинки', 'антидрожание изображения', 'антидрожание',
                              'стабилизации изображения', 'стабилизация изображения', 'технология снижения вибрации'],
    'форматы видео': ['форматы видео', 'поддерживающие форматы видео', 'форматы видеосъемки'],
    'цокль': ['цокль', 'гнездо', 'цокл', 'разъем'],
    'цвет лампочки': ['цвет лампочки', 'цвет стекла'],
    'цвет света': ['цвет света', 'цветовая температура', 'оттенок света', 'цветовой оттенок'],
    'срок службы': ['срок службы', 'время эксплуатации', 'рабочий период'],
    'колличество источников света': ['колличество источников света', 'колличество ламп', 'число источников освещения',
                                     'количество светильников'],
    'максимальная освещаемая территория': ['максимальная освещаемая территория', 'площадь освещения',
                                           'площадь охватываемая', "покрытие светом"],
    'пульсация': ['пульсация', "мерцание света", "фликеринг", "сверкание света", "переменное освещение"],
    'диапозон рабочих температур': ['диапозон рабочих температур', "рабочий температурный диапазон",
                                    "диапазон рабочих условий", "рабочий диапазон температур",
                                    "диапазон температур эксплуатации"],
    'внутренние габариты': ['внутренние габариты', "внутренние размеры", "внутренние размеры корпуса",
                            "внутренние размеры устройства", "внутренний объем"],
    'колличество кнопок': ['колличество кнопок', 'колличество переключатей', 'колличество клавиш'],
    'номинальный ток': ['номинальный ток', "рейтинговый ток", "номинальный электрический ток", "допустимый ток",
                        "максимальный ток", "электрическая нагрузка", "допустимая мощность", "нагрузочная способность"],
    'гнезда': ['гнезда', "контакты розеток", "электрические контакты", "контактные гнезда", "розеточные гнезда",
               "электрические выводы", "контактные зоны"],
    'полоса частот': ['полоса частот', "частотный диапазон", "рабочий диапазон частот",
                      "диапазон частотной характеристики", "диапазон частотных колебаний", "частотный спектр"],
    'разрешение печати': ['разрешение печати', 'качество печати', "точность печати", "детализация печати",
                          "плотность точек"],
    'скорость печати': ['скорость печати', 'темп печати', 'быстрота набора', 'скорость набора',
                        'скорость набора текста'],
    'технология подключения': ['технология подключения', 'методы подключения', 'техника подключения',
                               'способы подключения', 'поддерживаемые способы подключения'],
    'двусторонняя печать': ['двусторонняя печать', 'двухсторонняя печать', 'двойная печать', 'печать на обеих',
                            'двухсторонний вывод'],
    'поддерживаемые форматы бумаг': ['поддерживаемые форматы бумаг', 'форматы бумаг', 'формат бумаг', 'размеры бумаг',
                                     'размеры листов', 'типы бумаг'],
    'технологии печати': ['технологии печати', 'технологии лазерной печати', 'технология печати'],
    'цветная печать': ['цветная печать', 'печать в цвете', 'цветной вывод', 'цветопечать', 'полноцветная печать'],
    'поддерживаемая плотность носителей': ['поддерживаемая плотность носителей', 'допустимая плотность', 'плотность'],
    'издательский дом': ['издательский дом', 'издательская фирма', 'издательство', 'издательский комплекс',
                         'издательское предприятие'],
    'кол-во игроков': ['кол-во игроков', 'количество игроков', 'количество участников', 'число игроков',
                       'количество играющих', 'число участников'],
    'время игры': ['время игры', 'продолжительность игры', 'длительность игры', 'время проведения игры'],
    'ограничения по возрасту': ['ограничения по возрасту', 'возрастные ограничения', 'рекомендуемый возраст'],
    'жанр': ['жанр', 'жанровость'],
    'безопастность': ['безопастность'],
    'проводник': ['проводник'],
    'изоляция': ['изоляция'],
    'экран': ['экран', 'экран провода', 'экранирование проводов', 'экранирование'],
    'электрическое сопротивление': ['электрическое сопротивление', 'электрическая сопротивляемость',
                                    'электрическая резистивность'],
    'электрическая емкость': ['электрическая емкость', 'электроемкость', 'ёмкость проводников', 'ёмкость'],
    'скорость распространения': ['скорость распространения', 'скорость распространения тока', 'скорость передачи'],
    'рабочее напряжение': ['рабочее напряжение', 'максимальное напряжение'],
    'количество тостов': ['количество тостов', 'число тостов', 'кол-во тостов'],
    'стандарт wifi': ['стандарт wifi', 'стандарт беспроводной связи Wi-Fi', 'Wi-Fi технология', 'протокол Wi-Fi',
                      'спецификация Wi-Fi'],
    'максимальная скорость интернета': ['максимальная скорость интернета', 'максимальная пропускная способность',
                                        'скорость передачи данных', 'максимальная скорость',
                                        'скорость интернет-соединения'],
    'диапазоны частот': ['диапазоны частот', 'частотный диапазон', 'диапазон частотных волн', 'спектр частот'],
    'порты': ['порты', 'разъемы', 'интерфейсы', 'коннекторы'],
    'язык игры': ['язык игры', 'язык', 'локализация', 'перевод на'],
    'материал на ощупь': ['материал на ощупь', 'ткань', 'мягкая', 'пластик', 'плюш', 'резин'],
    'минимальная воспроизводимая частота': ['минимальная воспроизводимая частота', 'минимальная частота',
                                            'наименьшая частота'],
    'максимальная воспроизводимая частота': ['максимальная воспроизводимая частота', 'максимальная частота',
                                             'наибольшая частота'],
    'сопротивление': ['сопротивление', 'импеданс', 'электрическое сопротивление'],
    'чувствительность': ['чувствительность', 'эффективность звук', 'уровень громкости', 'звуковая мощность'],
    'микрофон': ['микрофон', 'есть микрофон', 'наличие микрофона'],
    'bluetooth': ['bluetooth'],
    'способ передачи сигнала': ['способ передачи сигнала', 'технология передачи сигнала', 'передача сигнала',
                                'способ подключения'],
    'поддержка карты памяти': ['поддержка карты памяти', 'карты памяти', 'разъем для карт', 'разъем карт'],
    'принцип работы': ['принцип работы', 'принцип действия', 'принцип микроф', 'способ работы'],
    'колки': ['колки', 'струнодержатели', 'крепление струн', 'колк'],
    'мензура': ['мензура', 'длинна', 'размер'],
    'звукосниматель': ['звукосниматель', 'тонозаборник', 'звукоприемник'],
    'размер в четвертях': ['размер в четвертях', ],
    'подбородник': ['подбородник', 'подподкова', 'подбородная'],
    'смычок': ['смычок', 'артикуляция', 'смычк'],
    'октавы': ['октавы', 'октав', 'октавный диапазон'],
    'чувствительность клавиш': ['чувствительность клавиш', 'чувствительность к нажатию', 'чувствительность нажатия',
                                'отзывчивость клав'],
    'педали': ['педали', 'педаль'],
    'тембр': ['тембр', 'звуковой окрас', 'тональность'],
    'строй': ['строй', 'аккордность', 'тональность'],
    'части': ['мундштук', 'трубка-горлышко', 'корпус инструмента', 'клапаны', 'клавиши', 'звуковая дырка', 'отверстие',
              'губная пластина', 'губная дырка', 'расширительная колба'],
    'пэд': ['пэд', 'перкуссионные подушки', 'чинели', 'чайны', 'тарелки'],
    'левая рука': ['левая рука', 'левой руке', 'левая'],
    'правая рука': ['правая рука', 'правой руке', 'правая'],
    'регистры': ['сопрано', 'меццо-сопрано', 'контральто', 'тенор', 'баритон', 'бас'],
    'ряды': ['ряды', 'клавиши', 'гриф']

}


def download_pic(url: str):
    response = requests.get(url)

    # Получаем имя файла из ссылки
    filename = url.split('/')[-1]
    print(os.path.join(BASE_DIR, f'static/images/{filename}'))

    # Проверяем, существует ли уже файл с таким именем
    if os.path.isfile(os.path.join(BASE_DIR, f'static/images/{filename}')):
        return filename

    # Если формат картинки webp, меняем на другой формат
    if response.headers.get('content-type') == 'image/webp':
        filename = filename.replace('.webp', '.jpg')
        temp_filepath = os.path.join(tempfile.gettempdir(), filename)
        with open(temp_filepath, 'wb') as file:
            file.write(response.content)
        image = Image.open(temp_filepath).convert('RGB')
        image.save(os.path.join(BASE_DIR, f'static/images/{filename}').replace('\\', '/'), 'JPEG')
        os.remove(temp_filepath)
    else:
        with open(os.path.join(BASE_DIR, f'static/images/{filename}').replace('\\', '/'), 'wb') as file:
            file.write(response.content)

    return filename


def update_pic(file):
    file_name = file.name
    pref = file_name[file_name.rfind('.'):]

    if pref.lower() == '.webp':
        print('WEBP TO JPG UPDATE')
        new_name = f'{str(randint(1000, 1000000))}.jpg'
        try:
            image = Image.open(file).convert("RGB")
            image.save(os.path.join(BASE_DIR, f'static/images/{new_name}'), "JPEG")
        except (IOError, OSError):
            return None
    else:
        new_name = f'{str(randint(1000, 1000000))}{pref}'
        try:
            with open(os.path.join(BASE_DIR, f'static/images/{new_name}'), "wb") as out:
                out.write(file.read())
        except IOError:
            return None

    return new_name

def download_file(file):
    file_name = file.name
    file_dir = os.path.join(BASE_DIR, 'static/files').replace('\\', '/')
    file_path = os.path.join(file_dir, file_name).replace('\\', '/')

    if 'xlsx' in file_name or 'csv' in file_name:
        # Проверка наличия файла с таким именем
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
            except:
                pass
            with open(file_path, "wb") as out:
                out.write(file.read())

            return file_name

            # Генерация нового имени файла
            # new_file_name = generate_new_filename(file_name)
            # print(new_file_name)
            # new_file_path = os.path.join(file_dir, new_file_name).replace('\\', '/')
            # new_temp_file_path = os.path.join(file_dir, f"temp_{new_file_name}").replace('\\', '/')
            #
            # # Запись нового файла во временную директорию
            # with open(new_temp_file_path, "wb") as out:
            #     out.write(file.read())
            #
            # file.close()
            # # Удаление исходного файла
            # os.remove(file_path)
            #
            # # Перемещение нового файла из временной директории
            # shutil.move(new_temp_file_path, new_file_path)

            # return new_file_path

        else:
            # Запись нового файла
            with open(file_path, "wb") as out:
                out.write(file.read())

            return file_name
    else:
        file_path = os.path.join(BASE_DIR, f'static/files/{file.name}')
        with open(file_path, "wb") as out:
            out.write(file.read())

        # Открываем xls-файл с помощью xlrd и считываем данные
        xls_filename = file_path
        workbook = xlrd.open_workbook(xls_filename)
        sheet = workbook.sheet_by_index(0)
        data = [sheet.row_values(i) for i in range(sheet.nrows)]

        # Создаем новый xlsx-файл и записываем данные
        xlsx_filename = os.path.join(BASE_DIR, f'static/files/{file.name[:file.name.find(".")]}.xlsx')
        new_wb = Workbook()
        new_ws = new_wb.active

        for row in data:
            new_ws.append(row)

        new_wb.save(xlsx_filename)
        os.remove(xls_filename)

        return f'{file.name[:file.name.find(".")]}.xlsx'

def generate_new_filename(file_path):
    file_dir, file_name = os.path.split(file_path)
    file_base, file_ext = os.path.splitext(file_name)
    new_file_name = file_base + "_old" + file_ext
    return new_file_name



def extract_first_number(string):
    pattern = r'\d+(\.\d+)?'  # Регулярное выражение для поиска чисел

    match = re.search(pattern, string)
    if match:
        number_str = match.group()
        number = float(number_str)
        return number
    else:
        return None


def is_range_ok(key, value, res):
    page = price_validator(value)
    req = price_validator(res.get(key, None))
    percentage = (abs(req - page) / req) * 100
    if percentage >= 30:
        return False
    else:
        return True


def change_pic(old):
    path = (os.path.join(BASE_DIR, f'static\\images\\{old}')).replace('\\', '/')
    try:
        os.remove(path)
    except:
        return None