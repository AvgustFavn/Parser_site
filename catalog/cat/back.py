# coding: utf8
import ast
import datetime
import hashlib
import json
import random
import re
import time
from urllib.parse import quote

import requests
from asgiref.sync import sync_to_async
from bs4 import BeautifulSoup
from django.forms import *
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import asyncio
from django.db import connection
import logging
from selenium.webdriver.support.wait import WebDriverWait
from cat.add_prod_module import add_prod_from_sites, get_alalogs, unique_prods, update_exist_prod_pars, pars_type_prod, \
    chat_get_type
from cat.models import *
from django.apps import apps
from django.db import models
from datetime import datetime
from cat.parsing_back import is_range_ok, download_pic

URLL = "https://api.openai.com/v1/chat/completions"

d = {
# 'Providers': 'Поставщики',
        'StoveAndOven': 'Духовка/ печь',
        'Fridges': 'Холодильник',
        'Dishwashers': 'Посудомойка',
        'ForDrinks': 'Устройства для напитков',
        'Grills': 'Гриль',
        'Toasters': 'Тостер',
        'Fryers': 'Фритюр',
        'Multicookers': 'Мультиварка',
        'KitchenScales': 'Кухонные весы',
        'WashingMachines': 'Стиральная машина',
        'Dryer': 'Сушилка',
        'Irons': 'Утюг',
        'VacuumCleaners': 'Пылесос',
        'RobotVacuumCleaner': 'Робот-пылесос',
        'WaterHeaters': 'Водо-нагреватель',
        'AirConditioners': 'Кондиционер',
        'Fans': 'Вентилятор',
        'Heaters': 'Обогреватель',
        'Sewing': 'Шитье',
        'HairStylingDrying': 'Для ухода за волосами',
        'ElectricShavers': 'Электробритва',
        'PhotoEquipment': 'Фотоаппараты и экипировка к нему',
        'Microwave': 'Микроволновка',
        'Lighting': 'Освещение',
        'Sockets': 'Розетки и переключатели',
        'Printers': 'Принтеры',
        'BoardGames': 'Настольные игры',
        'ChildToys': 'Детские игрушки',
        'Wires': 'Кабели',
        'Routers': 'Роутер',
        'Headset': 'Наушники',
        'Speakers': 'Колонки и акустика',
        'Microphone': 'Микрофон',
        'StringedInstruments': 'Струнные муз. инструменты',
        'KeyboardInstruments': 'Клавишные муз. инструменты',
        'WindInstruments': 'Духовые муз. инструменты',
        'PercussionInstruments': 'Ударные муз. инструменты',
        'Accordion': 'Аккордион',
        'SportsThings': 'Спорт-товары',
        'Clothes': 'Одежда',
        'MusicAccessories': 'Музыкальные аксессуары',
        'Another': 'Другое'

    }



c = {   'картинка': 'pic',
        'артикул': 'art',
        'наименование': 'name',
        'описание': 'descr',
        'цена': 'price',
        'доcnупность': 'available',
        'жанр': 'genre',
        'количество конфорок': 'burners',
        'вид топлива': 'fuel',
        'функция тайм-лапс': {'timelapse': 'bool'},
        'объективы': 'lens',
        'максимальный размер памяти в карте памяти': 'maximum_memory_card_size',
        'емкость для пыли': 'dust_capacity',
        'правая сторона аккордеона': 'right',
        'смычок': 'bow',
        'наличие микрофона': {'mike': 'bool'},
        'напряжение питания': 'supply_voltage',
        'поддерживаемые форматы бумаги': 'supported_paper_sizes',
        'максимальное давление воды': 'max_water_pressure',
        'уровень шума': 'noise_level',
        'цветная печать': 'print_color',
        'педали (ударные инструменты)': 'pads',
        'тембр': 'timbres',
        'проводник (кабель)': 'conductor',
        'измерение объема жидкости': {'liquid_volume_measurement': 'bool'},
        'материал лезвия': 'blade_material',
        'поддерживаемая плотность бумаги': 'supported_media_weights',
        'разморозка': {'defrosting': 'bool'},
        'скорости': 'speeds',
        'изоляция (кабели)': 'insulation',
        'тип батареи': 'battery_type',
        'самозатачиваемые лезвия': {'self_sharpening_knives': 'bool'},
        'технология печати': 'print_technology',
        'тип кофе (зерна, растромое и т.д.)': 'type_of_coffee',
        'время до полного заряда': 'сharging_time',
        'самоочистка (утюг)': 'self_cleaning',
        'максимальный вес': 'maximum_weight',
        'стабилизация картинки (фотоаппарат)': {'image_stabilization':'bool'},
        'управление (дистанционно или...)': 'control',
        'слот для карты памяти': {'memory_cards_slot': 'bool'},
        'наличие таймера': {'timer': 'bool'},
        'теплообменник': {'recycling': 'bool'},
        'пропускная способность': 'bandwidth',
        'градус спектра света': 'spectrum_quality',
        'максимальное время таймера': 'max_timer',
        'радиус работы bluetooth': 'radius',
        'количество октав': 'octaves',
        'количество led': 'num_leds',
        'материал подошвы утюг': 'sole_material',
        'тип сушки': 'drying_type',
        'расход газа/топлива': 'gas_consumption',
        'номинальный ток': 'rated_current',
        'потребление сушки': 'dry_class',
        'кол-во источников освещения': 'num_light_sources',
        'двусторонняя печать': {'duplex_printing': 'bool'},
        'экран (кабель)': 'screen',
        'время нагрева устройства (для волос)': 'heating_time',
        'охлаждающая способность': 'cooling_capacity',
        'регулировка температуры': 'temp_step_adjustment',
        'чаша весов (мл, л)': 'bowl',
        'лимит веса': 'weighing_limit',
        'вентелятор в обогревателе': {'fan': 'bool'},
        'авто-отключение': {'auto_shutdown': 'bool'},
        'беспроводной': {'wireless': 'bool'},
        'подставка для подбородка (скрипка)': 'chinrest',
        'цокль': 'plinth',
        'поддержка карты памяти': 'supported_memory_cards',
        'наличие фильтра': {'filter': 'bool'},
        'рекомендованый радиус отопления/ охлаждения': 'recommended_room_area',
        'минимальная повторяемая частота': 'minimum_repeatable_frequency',
        'внутренние размеры': 'internal_dimensions',
        'максимальная территория освещения': 'max_lighting_area',
        'кол-во четвертей': 'quarters',
        'форматы фото (фотоаппарат: row, jpeg и т.д.)': 'image_formats',
        'вспышка': {'flash': 'bool'},
        'мощность передатчика': 'transmitter_power',
        'доступные разьемы': 'ports',
        'поддержание температуры': {'temperature_maintenance': 'bool'},
        'максимальная производительность': 'maximum_performance',
        'выдержка (фотоапп.)': 'excerpt',
        'наличие сканнера': {'scanner': 'bool'},
        'сколько места для тостов': 'numbers_of_toasts',
        'сфера применения': 'scope_of_application',
        'скорость печати': 'print_speed',
        'цвет': 'color',
        'полнокадровый': {'full_frame': 'bool'},
        'максимальный вес для сушки': 'maximum_weight_to_dry',
        'воздушный поток': 'air_flow',
        'электрическая емкость': 'electrical_capacitance',
        'станция для робота-пылесоса': {'station': 'bool'},
        'рабочая температура (кабель)': 'temp',
        'разрешение печати': 'print_resolution',
        'подсветка': {'backlight': 'bool'},
        'степени обжарки (тостер)': 'browning_levels',
        'насадки': 'nozzles',
        'макс. скорость': 'max_speed',
        'общее число мегапикселей матрицы': 'total_number_megapix_matrix',
        'заземление': {'grounding': 'bool'},
        'трубы для пылесоса (насадки)': 'pipe',
        'мензура': 'mensura',
        'стандарт wifi': 'standard',
        'безопастность (роутер)': 'security',
        'максимальное разрешение': 'maximum_resolution',
        'компания': 'company',
        'чувствительность клавиш': 'key_sensitivity',
        'bluetooth': {'bluetooth': 'bool'},
        'отделение для аксессуаров': 'сompartment_for_accessories',
        'процессор': 'cpu',
        'интенсивность осушения': 'dehumidification_intensity',
        'объем духовки': 'oven_volume',
        'url': 'url',
        'минимальная температура': 'min_temperature',
        'мощность на одну конфорку': 'power_per_burner',
        'тип источника света': 'light_source_type',
        'регулируемый термостат': {'adjustable_thermostat': 'bool'},
        'звукосниматель': 'pickup',
        'диаметр поддона': 'pallet_diameter',
        'автоматический слив масла': {'auto_oil_drain': 'bool'},
        'диафрагма': 'diaphragm',
        'язык': 'lang',
        'задержка старта': {'delay_start': 'bool'},
        'детали': 'parts',
        'ряды аккордеона': 'ranks',
        'в комплекте': 'equipment',
        'тип подключения': 'connection_type',
        'форма лампы': 'lamp_shape',
        'дисплей': 'display',
        'вместимость контейнера': 'container_capacity',
        'количество батареек': 'number_of_batteries',
        'дальность вспышки': 'flash_range',
        'крышка': {'lid': 'bool'},
        'Пульсация': 'ripples',
        'страна производитель': 'manufacturer_country',
        'педали': {'pedals': 'bool'},
        'чувствительность': 'sensitivity',
        'диапазоны': 'ranges',
        'душевая головка': {'shower_head': 'bool'},
        'значение диафрагмы': 'aperture_value',
        'потребление топлива': 'fuel_consumption',
        'издательство': 'publishing_house',
        'двойная игла': 'double_needle',
        'тип матрицы': 'matrix_type',
        'электрическое сопротивление': 'electrical_resistance',
        'объем': 'volume',
        'запланированная чистка': {'scheduled_cleaning': 'bool'},
        'трафарет': {'stencil': 'bool'},
        'размеры': 'sizes',
        'рабочие температуры': 'operating_temperatures',
        'регистр': 'register',
        'тип загрузки': 'download_type',
        'антипригарное покрытие': {'non_stick_coating': 'bool'},
        'Тип машинки': 'machine_type',
        'фактор кропа': 'crop_factor',
        'USB': {'usb': 'bool'},
        'колки струн. инструментов': 'pegs',
        'дисплей с температурой': {'temperature_display': 'bool'},
        'время игры': 'game_time',
        'тип защиты от протечек': 'leak_protection_type',
        'левая сторона аккордиона': 'left',
        'педаль': 'pedal',
        'мощность замораживания': 'freezing_power',
        'максимальная скорость барабана стирки': 'max_spin_speed',
        'поддержка 1080p': 'q1080_support',
        'максимальная повторяемая частота': 'maximum_repeatable_frequency',
        'точность взвешивания': 'weighing_accuracy',
        'настройка громкости': 'volume_control',
        'размеры коробки': 'box_dimensions',
        'количество сегментов': 'segment_count',
        'регулировка интенсивности': 'intensity_adjustment',
        'уровень шума': 'noise_level',
        'количество выходов': 'output_count',
        'частота процессора': 'processor_frequency',
        'тип двигателя': 'engine_type',
        'защитный экран': 'protective_screen',
        'тип вставки': 'insert_type',
        'физический размер матрицы': 'physical_matrix_size',
        'объем водного резервуара': 'water_tank_volume',
        'максимальное разрешение': 'max_resolution',
        'тепловыделение': 'heat_output',
        'зум': 'zoom',
        'тип щетки': 'brush_type',
        'мощность (ватт)': 'wattage',
        'емкость холодильника': 'refrigerator_capacity',
        'частота обновления': 'refresh_rate',
        'фокусное расстояние': 'focal_length',
        'скорость процессора': 'processor_speed',
        'соединение': 'connectivity',
        'давление': 'pressure',
        'интерфейс': 'interface',
        'тип сенсора': 'sensor_type',
        'время работы от батареи': 'battery_life',
        'материал рамы': 'frame_material',
        'источник питания': 'power_supply',
        'размер дисплея': 'display_size',
        'вес': 'weight',
        'разрешение экрана': 'screen_resolution',
        'тип процессора': 'processor_type',
        'емкость аккумулятора': 'battery_capacity',
        'максимальная грузоподъемность': 'max_load_capacity',
        'размер экрана': 'screen_size',
        'водонепроницаемость': 'water_resistance',
        'угол обзора': 'viewing_angle',
        'память': 'memory',
        'гарантия': 'warranty',
        'емкость': 'capacity',
        'частотная характеристика': 'frequency_response',
        'беспроводная технология': 'wireless_technology',
        'материал': 'material',
        'максимальная потребляемая мощность': 'max_power_consumption',
        'класс энергопотребления': 'energy_class',
        'максимальная температура': 'max_temperature',
    }

USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 Edg/87.0.664.66',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36 OPR/73.0.3856.329']


opera_driver_path = '/home/rdp-user/Documents/catalog_site/catalog/operadriver_linux64/chromedriver'
# opera_driver_path = 'C:/Users/avgus/Documents/py_shit/catalog_site/catalog/operadriver_linux64/chromedriver.exe'
options = Options()
options.add_argument(f"--user-agent={random.choice(USER_AGENTS)}")
options.add_argument("start-maximized")
options.add_argument("disable-infobars") 
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument('--ignore-certificate-errors')
options.add_argument('--ignore-ssl-errors')
caps = webdriver.DesiredCapabilities.CHROME.copy()
caps['acceptInsecureCerts'] = True
caps['acceptSslCerts'] = True
# options.headless = True
driver = webdriver.Chrome(executable_path=opera_driver_path, chrome_options=options, desired_capabilities=caps)
driver.implicitly_wait(12)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


async def run_add_prod_from_sites(datas, sites_datas=None, chars_p=None, req=None, url=None, status=None):
    logger.debug('run_add_prod_from_sites')
    await add_prod_from_sites(datas=datas, sites_datas=sites_datas, chars_p=chars_p, req=req, url=url, status=status)


async def run_pars_all(sites, products, res, req=None):
    logger.debug('run_pars_all')
    if ' ' in sites[0]:
        sites_list = sites[0].split()
    else:
        sites_list = sites

    if products != None:
        if '!' in products:
            products_list = products.split('!')
        else:
            products_list = [products, ]
    else:
        products_list = []

    products_list = [x for x in products_list if x.strip() != '']

    await pars_one_site(sites_list, products_list, res, req)

async def pars_one_site(url, prod_list, res=None, req=None):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    session = requests.session()
    session.headers[
        'User-Agent'] = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0'
    if not prod_list:
        for u in url:
            if u.find('invask.ru') != -1:
                print('Начинаем')
                name = res.get('тип товара', None)
                sec_name = res.get('доп. название товара', None)
                if sec_name:
                    name = sec_name
                rs = driver.get(f'https://invask.ru/search?term={name}')
                html = driver.execute_script("return document.documentElement.outerHTML")
                soup = BeautifulSoup(html, 'lxml')
                prod_sites = soup.find_all("div", class_="product-desc")
                urls_list = []
                for p in prod_sites:
                    u = p.find('a').get_attribute_list('href')[0]
                    urls_list.append(u)

                urls_list = list(set(urls_list))
                for u in urls_list:
                    rs = driver.get(u)
                    html = driver.execute_script("return document.documentElement.outerHTML")
                    so = BeautifulSoup(html, 'lxml')
                    try:
                        status = so.find("div", class_="product-stock-status-text available").text
                    except:
                        try:
                            status = so.find("div", class_="product-stock-status-text not-available").text
                        except:
                            status = 'нет'
                    title = so.find("h1", class_="product-title").string
                    task = asyncio.create_task(unique_prods(title))
                    ok = await task

                    chars_p = {}
                    if 'налич' in status and not 'нет' in status:  # если в наличии
                        status = 'В наличии'
                    else:
                        status = 'Нет в наличии'
                    res.pop('sites', None)
                    res.pop('тип товара', None)
                    try:
                        descrs = so.find("div", class_="mb-5").text
                    except:
                        try:
                            descrs = so.find("div", class_="row mb-4").text
                        except:
                            descrs = ''

                    price = so.find("ins", class_="new-price ls-50").string
                    if res.get('цена', None):
                        r = is_range_ok('цена', price, res)
                        if not r:
                            continue
                        res.pop('цена', None)

                    img = so.find("figure", class_="product-image")
                    img = img.find('img').get_attribute_list('src')[0]
                    try:
                        try:
                            chs = so.find("ul", class_="list-type-check").text
                            # chars = find_characteristics(descrs)
                            chars = chat_get_chars(title, f'{descrs} {chs}')
                            print('chs', chs)
                        except:
                            chars = chat_get_chars(title, descrs)

                        print('chars', chars)
                    except:
                        chars = {}

                    if not chars:
                        chars = {}
                    pic_name = download_pic(f'https://invask.ru{img}')

                    if ok:
                        price = await sync_to_async(price_validator)(price)
                        print(f'Цена {price}')
                        await sync_to_async(update_exist_prod_pars)({'name': title,
                                                                     'type_': chat_get_type(title, descrs),
                                                                     'price': price, 'available': status, 'chars': chars}, url=u)
                        continue

                    try:
                        await run_add_prod_from_sites(datas=[title, price, chars, pic_name, descrs], req=req,
                                                      chars_p=chars_p, url=u, status=status)
                    finally:
                        pass

            elif u.find('muztorg.ru') != -1:
                chars_p = {}
                name = res.get('тип товара', None)
                sec_name = res.get('доп. название товара', None)
                if sec_name:
                    name = sec_name
                rs = driver.get(f'https://www.muztorg.ru/search/{name}?in-stock=1&pre-order=1&per-page=96')
                html = driver.execute_script("return document.documentElement.outerHTML")
                soup = BeautifulSoup(html, 'lxml')
                prod_sites = soup.find_all("div", class_="title")
                urls_list = []
                for p in prod_sites:
                    urll = p.find('a').get_attribute_list('href')[0]
                    urls_list.append(f'https://www.muztorg.ru{urll}')

                urls_list = list(set(urls_list))
                for ur in urls_list:
                    rs = driver.get(ur)
                    html = driver.execute_script("return document.documentElement.outerHTML")
                    so = BeautifulSoup(html, 'lxml')
                    try:
                        status = so.find("div", class_="product-info__i _available").text
                    except:
                        try:
                            status = so.find("div",  class_="product-info__i").text
                        except:
                            status = 'Под заказ'


                    res.pop('sites', None)
                    res.pop('тип товара', None)
                    try:
                        price = so.find("p", class_="price-value-gtm origin hidden").text
                    except:
                        try:
                            price = so.find("p", class_="price-value origin").text
                            price = price_validator(price)
                        except:
                            price = None

                    try:
                        descrs = so.find("div", itemprop="description").text
                    except:
                        try:
                            descrs = so.find("div", class_='product-info__i _description').text
                        except:
                            try:
                                descrs = so.find("div", class_='product-info__i _description').text
                            except:
                                descrs = ''


                    if res.get('цена', None):
                        r = is_range_ok('цена', price, res)
                        if not r:
                            continue

                        res.pop('цена', None)

                    try:
                        title = so.find("h1", class_="product-title").text
                    except:
                        try:
                            title = so.find("span", itemprop="name").text
                        except:
                            continue

                    loop = asyncio.get_event_loop()
                    ok = await loop.create_task(unique_prods(title))

                    if 'налич' in status:  # если в наличии
                        status = 'В наличии'
                    else:
                        status = 'Под заказ'


                    img = so.find("img", id='slide1')
                    if img:
                        img = img.get_attribute_list('src')[0]
                        print(img)
                        pic_name = download_pic(img)
                    else:
                        pic_name = 'Н.Д.'

                    try:
                        try:
                            chs = so.find("div", id="myTabContent").text
                            # chars = find_characteristics(descrs)
                            if len(chs) > 1500:
                                chars = chat_get_chars(title, descrs)
                            else:
                                chars = chat_get_chars(title, f'{descrs} {chs}')
                                print('chs', chs)
                        except:
                            chars = chat_get_chars(title, descrs)

                        print('chars', chars)
                    except:
                        chars = {}

                    if not chars:
                        chars = {}

                    if ok:
                        price = await sync_to_async(price_validator)(price)
                        await sync_to_async(update_exist_prod_pars)({'name': title,
                                                                     'type_': chat_get_type(title, descrs),
                                                                     'price': price, 'available': status, 'chars': chars}, url=ur)
                        continue

                    try:
                        await run_add_prod_from_sites(datas=[title, price, chars, pic_name, descrs], req=req,
                                                      chars_p=chars_p, url=u, status=status)
                    finally:
                        pass

            elif u.find('ltm-music.ru') != -1:
                name = res.get('тип товара')
                sec_name = res.get('доп. название товара', None)
                if sec_name:
                    name = sec_name
                try:
                    driver.get(f"https://ltm-music.ru/#/query={name}&skip=0&limit=24")
                except:
                    try:
                        driver.get(f"https://ltm-music.ru/#/query={name}&skip=0&limit=24")
                    except:
                        driver.get(f'https://ltm-music.ru/search?q={name}')
                        wait = WebDriverWait(driver, 20)

                html = driver.execute_script("return document.documentElement.outerHTML")
                soup = BeautifulSoup(html, 'lxml')
                prod_sites = soup.find_all("a", class_="quick-view")
                urls_list = []
                for p in prod_sites:
                    url = p.get_attribute_list('href')[0]
                    urls_list.append(f'https://ltm-music.ru{url}')

                urls_list = list(set(urls_list))
                for ul in urls_list:
                    chars_p = {}
                    rs = session.get(ul)
                    rs.raise_for_status()
                    page = rs.text
                    so = BeautifulSoup(page, 'lxml')
                    status = so.find("div", class_="available clearfix").text
                    res.pop('sites', None)
                    res.pop('тип товара', None)
                    try:
                        price = so.find("div", class_="price price-offer-473711 price-selected").text
                    except:
                        try:
                            price = so.find("div", class_="price-block-left").text
                        except:
                            price = so.find("div", class_="price-main").text

                    try:
                        descrs = so.find("div", class_="text-in").text
                    except:
                        descrs = 'Н.Д.'

                    if res.get('цена', None):
                        r = is_range_ok('цена', price, res)
                        if not r:
                            continue

                        res.pop('цена', None)

                    title = so.find("div", class_="product-title").find('h1').string
                    loop = asyncio.get_event_loop()
                    ok = await loop.create_task(unique_prods(title))

                    if 'осталось' in status:
                        status = 'Есть остатки'
                    elif 'наличии' in status:
                        status = 'В наличии'
                    else:
                        status = 'Под заказ'

                    try:
                        img = so.find('a', class_='fancybox').find('img').get_attribute_list('src')[0]
                    except:
                        try:
                            img = so.find('a', class_='fancybox').get_attribute_list('href')[0]
                        except:
                            img = None

                    if img:
                        pic_name = download_pic(f'https://ltm-music.ru{img}')

                    else:
                        pic_name = 'Н.Д.'

                    try:
                        try:
                            chs = so.find("div", class_="properties").text
                            # chars = find_characteristics(descrs)
                            chars = chat_get_chars(title, f'{descrs} {chs}')
                            print('chs', chs)
                        except:
                            chars = chat_get_chars(title, descrs)

                        print('chars', chars)
                    except:
                        chars = {}

                    if not chars:
                        chars = {}

                    if ok:
                        price = await sync_to_async(price_validator)(price)
                        await sync_to_async(update_exist_prod_pars)({'name': title,
                                                                     'type_': chat_get_type(title, descrs),
                                                                     'price': price, 'available': status, 'chars': chars}, url=ul)
                        continue

                    try:
                        await run_add_prod_from_sites(datas=[title, price, chars, pic_name, descrs], req=req,
                                                      chars_p=chars_p, url=u, status=status)
                    finally:
                        pass
            # ??????
            elif u.find('citilink.ru') != -1:
                name = res.get('тип товара')
                sec_name = res.get('доп. название товара', None)
                if sec_name:
                    name = sec_name
                try:
                    driver.get(f"https://www.citilink.ru/search/?text={quote(name.encode('utf-8'))}")
                except:
                    driver.get(f"https://www.citilink.ru/search/?text={quote(name.encode('utf-8'))}")

                html = driver.execute_script("return document.documentElement.outerHTML")
                soup = BeautifulSoup(html, 'lxml')
                print('Получили страницу товаров')
                prod_sites = soup.find_all("a", class_="app-catalog-9gnskf e1259i3g0")
                urls_list = []
                for p in prod_sites:
                    url = p.get_attribute_list('href')[0]
                    urls_list.append(f'https://www.citilink.ru{url}')


                if not urls_list:
                    time.sleep(3)
                    try:
                        driver.get(f"https://www.citilink.ru/search/?text={quote(name.encode('utf-8'))}")
                    except:
                        driver.get(f"https://www.citilink.ru/search/?text={quote(name.encode('utf-8'))}")

                    html = driver.execute_script("return document.documentElement.outerHTML")
                    soup = BeautifulSoup(html, 'lxml')
                    prod_sites = soup.find_all("a", class_="app-catalog-9gnskf e1259i3g0")
                    urls_list = []
                    for p in prod_sites:
                        url = p.get_attribute_list('href')[0]
                        urls_list.append(f'https://www.citilink.ru{url}')

                time.sleep(8)
                print(urls_list)
                for u in urls_list:
                    try:
                        driver.get(f'{u}')
                    except:
                        try:
                            driver.get(f'{u}')
                        except:
                            continue
                    html = driver.execute_script("return document.documentElement.outerHTML")
                    so = BeautifulSoup(html, 'lxml')
                    try:
                        title = so.find("h1").text
                    except:
                        try:
                            title = so.find('h1', color="Main").text
                        except:
                            try:
                                title = so.find('h1', class_='e1ubbx7u0 eml1k9j0 app-catalog-tn2wxd e1gjr6xo0').text
                            except:
                                continue

                    ok = await unique_prods(title)
                    try:
                        status = so.find('span', class_='e1rezvh20 e106ikdt0 app-catalog-oicqvy e1gjr6xo0').text
                    except:
                        status = ''

                    if status and status.find('Нет'):
                        status = 'Нет в наличии'
                    else:
                        status = 'В наличии'

                    try:
                        price = so.find('span', class_='e1j9birj0 e106ikdt0 app-catalog-1f8xctp e1gjr6xo0').text
                    except:
                        try:
                            price = so.find('span', class_="app-catalog-0 eb8dq160").text
                        except:
                            price = None

                    try:
                        img = so.find('img',
                                      class_='ekkbt9g0 app-catalog-15kpwh2 e1fcwjnh0').get_attribute_list('src')[0]
                    except:
                        img_element = so.select_one('div.app-catalog-1igv0r1.e19l9blg0.is-selected img[src]')
                        img = img_element['src'] if img_element else None

                    try:
                        descrs = so.find('div', class_='e1viufof0 app-catalog-1tv8d3m e62ro310').text
                    except:
                        descrs = ''

                    print('Описание ', descrs)

                    try:
                        driver.get(f'{u}properties/')
                    except:
                        driver.get(f'{u}properties/')
                    html = driver.execute_script("return document.documentElement.outerHTML")
                    so = BeautifulSoup(html, 'lxml')
                    chs = ''
                    try:
                        try:
                            chs = so.find("ul", class_="app-catalog-rxgulu e1ckvoeh6").text
                            # chars = find_characteristics(descrs)
                            chars = chat_get_chars(title, f'{descrs} {chs}')
                            print('chs', chs)
                        except:
                            chars = chat_get_chars(title, descrs)

                        print('chars', chars)
                    except:
                        chars = {}

                    if not chars:
                        chars = {}

                    time.sleep(8)
                    if img:
                        pic_name = download_pic(f'{img}')
                    else:
                        pic_name = 'Н.Д.'
                    chars_p = {}

                    if ok:
                        price = await sync_to_async(price_validator)(price)
                        await sync_to_async(update_exist_prod_pars)({'name': title,
                                                                     'type_': chat_get_type(title, f'{sec_name} {chs}'),
                                                                     'price': price, 'available': status, 'chars': chars}, url=u)
                        continue

                    try:
                        await run_add_prod_from_sites(datas=[title, price, chars, pic_name, descrs], req=req, chars_p=chars_p,  url=u, status=status)
                    finally:
                        pass

                    time.sleep(10)


    else:
        for u in url:
            if u.find('invask.ru') != -1:
                for p in prod_list:
                    print(prod_list)
                    rs = session.get(f'https://invask.ru/search?term={p}')
                    rs.raise_for_status()
                    page = rs.text
                    soup = BeautifulSoup(page, 'lxml')
                    prod_sites = soup.find_all("div", class_="product-desc")
                    urls_list = []
                    for p in prod_sites:
                        url = p.find('a').get_attribute_list('href')[0]
                        urls_list.append(url)

                    urls_list = list(set(urls_list))
                for u in urls_list:
                    rs = session.get(u)
                    rs.raise_for_status()
                    page = rs.text
                    so = BeautifulSoup(page, 'lxml')
                    try:
                        status = so.find("div", class_="product-stock-status-text available").text
                    except:
                        try:
                            status = so.find("div", class_="product-stock-status-text not-available").text
                        except:
                            status = 'нет'

                    title = so.find("h1", class_="product-title").string

                    if 'налич' in status and not 'нет' in status:  # если в наличии
                        status = 'В наличии'
                    else:
                        status = 'Нет в наличии'
                    ok = await unique_prods(title)
                    price = so.find("ins", class_="new-price").string
                    img_div = so.find("figure", class_="product-image")
                    img = img_div.find("img").get_attribute_list('src')[0]

                    try:
                        descrs = so.find("div", class_="mb-5").text
                    except:
                        try:
                            descrs = so.find("div", class_="row mb-4").text
                        except:
                            descrs = ''

                    try:
                        try:
                            chs = so.find("ul", class_="list-type-check").text
                            # chars = find_characteristics(descrs)
                            chars = chat_get_chars(title, f'{descrs} {chs}')
                            print('chs', chs)
                        except:
                            chars = chat_get_chars(title, descrs)

                        print('chars', chars)
                    except:
                        chars = {}

                    if not chars:
                        chars = {}


                    if img:
                        pic_name = download_pic(f'https://invask.ru{img}')
                    else:
                        pic_name = 'Н.Д.'

                    if ok:
                        price = await sync_to_async(price_validator)(price)
                        print(f'Цена {price}')
                        await sync_to_async(update_exist_prod_pars)({'name': title,
                                                                     'type_': chat_get_type(title, descrs),
                                                                     'price': price, 'available': status, 'chars': chars}, url=u)
                        continue

                    await run_add_prod_from_sites(datas=[title, price, chars, pic_name, descrs], req=req, url=u, status=status)

            elif u.find('muztorg.ru') != -1:
                for p in prod_list:
                    rs = driver.get(f'https://www.muztorg.ru/search/{quote(p)}?in-stock=1&pre-order=1&per-page=96')
                    html = driver.execute_script("return document.documentElement.outerHTML")
                    soup = BeautifulSoup(html, 'lxml')

                    prod_sites = soup.find_all("div", class_="title")
                    urls_list = []
                    for p in prod_sites:
                        url = p.find('a').get_attribute_list('href')[0]
                        urls_list.append(url)

                    urls_list = list(set(urls_list))
                    for u in urls_list:
                        rs = driver.get(f'https://www.muztorg.ru{quote(u)}')
                        html = driver.execute_script("return document.documentElement.outerHTML")
                        so = BeautifulSoup(html, 'lxml')
                        try:
                            status = so.find("div", class_="product-info__i _available").text
                        except:
                            try:
                                status = so.find("div", class_="product-info__available").text
                            except:
                                status = 'налич'

                        try:
                            title = so.find("h1", class_="product-title").text
                        except:
                            try:
                                title = so.find("span", itemprop="name").text
                            except:
                                continue

                        if 'налич' in status:  # если в наличии
                            status = 'В наличии'
                        else:
                            status = 'Под заказ'

                        ok = await unique_prods(title)
                        price = so.find("p", class_="price-value-gtm origin hidden").string
                        img = so.find("img", id='slide1')
                            
                        try:
                            descrs = so.find("div", itemprop="description").text
                        except:
                            try:
                                descrs = so.find("div", class_='product-info__i _description').text
                            except:
                                try:
                                    descrs = so.find("div", class_='product-info__i _description').text
                                except:
                                    descrs = ''
                        l = []
                        if type(descrs) == type(['a']):
                            for d in descrs:
                                l.append(d.text)

                            descrs = ' '.join(l)

                        try:
                            try:
                                chs = so.find("div", id="myTabContent").text
                                # chars = find_characteristics(descrs)
                                if len(chs) > 1500:
                                    chars = chat_get_chars(title, descrs)
                                else:
                                    chars = chat_get_chars(title, f'{descrs} {chs}')
                                    print('chs', chs)
                            except:
                                chars = chat_get_chars(title, descrs)

                            print('chars', chars)
                        except:
                            chars = {}

                        if not chars:
                            chars = {}
                        if not chars:
                            chars = {}

                        if img:
                            img = img.get_attribute_list('src')[0]
                            print(img)
                            pic_name = download_pic(img)
                        else:
                            pic_name = 'Н.Д.'

                        if ok:
                            price = await sync_to_async(price_validator)(price)
                            await sync_to_async(update_exist_prod_pars)({'name': title,
                                                                         'type_': chat_get_type(title, descrs),
                                                                         'price': price, 'available': status,
                                                                         'chars': chars},
                                                                        url=f'https://www.muztorg.ru{quote(u)}')
                            continue

                        await run_add_prod_from_sites(datas=[title, price, chars, pic_name, descrs], url=f'https://www.muztorg.ru{quote(u)}', req=req, status=status)

            elif u.find('ltm-music.ru') != -1:
                for p in prod_list:
                    try:
                        driver.get(f'https://ltm-music.ru/search?q={p}')
                        wait = WebDriverWait(driver, 20)
                        html = driver.page_source
                    except:
                        try:
                            driver.get(f'https://ltm-music.ru/search?q={p}')
                            wait = WebDriverWait(driver, 20)
                            html = driver.page_source
                        except:
                            try:
                                driver.get(f'https://ltm-music.ru/search?q={p}')
                                wait = WebDriverWait(driver, 20)
                                html = driver.page_source
                            except:
                                continue
                    soup = BeautifulSoup(html, 'lxml')
                    hrefs = [link["href"] for link in soup.select("div.name-in a[href]")]
                    urls_list = []
                    for url in hrefs:
                        urls_list.append(f'https://ltm-music.ru{url}')

                    urls_list = list(set(urls_list))
                    for u in urls_list:
                        driver.get(u)
                        html = driver.execute_script("return document.documentElement.outerHTML")
                        so = BeautifulSoup(html, 'lxml')
                        title = so.find("div", class_="product-title").find('h1').string
                        status = so.find("div", class_="available clearfix").text
                        if 'осталось' in status:
                            status = 'Есть остатки'
                        elif 'наличии' in status:
                            status = 'В наличии'
                        else:
                            status = 'Под заказ'

                        ok = await unique_prods(title)
                        try:
                            price = so.find("div", class_="price price-offer-473711 price-selected").text
                        except:
                            try:
                                price = so.find("div", class_="price-block-left").text
                            except:
                                price = so.find("div", class_="price-main").text

                        try:
                            img = so.find('a', class_='fancybox').find('img').get_attribute_list('src')[0]
                        except:
                            try:
                                img = so.find('a', class_='fancybox').get_attribute_list('href')[0]
                            except:
                                img = None


                        try:
                            descrs = so.find("div", class_="text-in").text
                        except:
                            try:
                                descrs = so.find("div", class_="text").text
                            except:
                                descrs = None

                        try:
                            try:
                                chs = so.find("div", class_="properties").text
                                # chars = find_characteristics(descrs)
                                chars = chat_get_chars(title, f'{descrs} {chs}')
                                print('chs', chs)
                            except:
                                chars = chat_get_chars(title, descrs)

                            print('chars', chars)
                        except:
                            chars = {}

                        if not chars:
                            chars = {}

                        if img:
                            pic_name = download_pic(f'https://ltm-music.ru{img}')
                        else:
                            pic_name = 'Н.Д.'

                        if ok:
                            price = await sync_to_async(price_validator)(price)
                            await sync_to_async(update_exist_prod_pars)({'name': title,
                                                                         'type_': pars_type_prod(title, descrs),
                                                                         'price': price, 'available': status, 'chars': chars},
                                                                        url=u)
                            continue

                        await run_add_prod_from_sites([title, price, chars, pic_name, descrs], url=u, req=req, status=status)


            elif u.find('citilink.ru') != -1:
                for p in prod_list:
                    try:
                        driver.get(f"https://www.citilink.ru/search/?text={quote(p)}")
                    except:
                        driver.get(f"https://www.citilink.ru/search/?text={quote(p)}")
                    html = driver.execute_script("return document.documentElement.outerHTML")
                    soup = BeautifulSoup(html, 'lxml')
                    prod_sites = soup.find_all("a", class_="app-catalog-9gnskf e1259i3g0")
                    urls_list = []
                    for pi in prod_sites:
                        url = pi.get_attribute_list('href')[0]
                        urls_list.append(f'https://www.citilink.ru{url}')

                    if not urls_list:
                        time.sleep(3)
                        try:
                            driver.get(f"https://www.citilink.ru/search/?text={quote(p)}")
                        except:
                            driver.get(f"https://www.citilink.ru/search/?text={quote(p)}")

                        html = driver.execute_script("return document.documentElement.outerHTML")
                        soup = BeautifulSoup(html, 'lxml')

                        prod_sites = soup.find_all("a", class_="app-catalog-9gnskf e1259i3g0")
                        urls_list = []
                        for p in prod_sites:
                            url = p.get_attribute_list('href')[0]
                            urls_list.append(f'https://www.citilink.ru{url}')

                    for u in urls_list:
                        time.sleep(random.randint(9, 17))
                        try:
                            driver.get(f'{u}')
                        except:
                            driver.get(f'{u}')
                        html = driver.execute_script("return document.documentElement.outerHTML")
                        so = BeautifulSoup(html, 'lxml')
                        title = so.find("h1").text
                        if not title:
                            title = so.find('h1', color="Main").text

                        try:
                            status = so.find('span', class_='e1rezvh20 e106ikdt0 app-catalog-oicqvy e1gjr6xo0').text
                        except:
                            status = ''

                        if status and status.find('Нет'):
                            status = 'Нет в наличии'
                        else:
                            status = 'В наличии'

                        ok = await unique_prods(title)
                        try:
                            price = so.find('span', class_='e1j9birj0 e106ikdt0 app-catalog-1f8xctp e1gjr6xo0').text
                        except:
                            try:
                                price = so.find('span', class_="app-catalog-0 eb8dq160").text
                            except:
                                price = None

                        try:
                            img = so.find('img',
                                          class_='ekkbt9g0 app-catalog-15kpwh2 e1fcwjnh0').get_attribute_list('src')[0]
                        except:
                            img_element = so.select_one('div.app-catalog-1igv0r1.e19l9blg0.is-selected img[src]')
                            img = img_element['src'] if img_element else None

                        try:
                            descrs = so.find('div', class_='e1viufof0 app-catalog-1tv8d3m e62ro310').text
                        except:
                            descrs = None

                        try:
                            driver.get(f'{u}properties/')
                        except:
                            driver.get(f'{u}properties/')
                        html = driver.execute_script("return document.documentElement.outerHTML")
                        so = BeautifulSoup(html, 'lxml')
                        try:
                            try:
                                chs = so.find("ul", class_="app-catalog-rxgulu e1ckvoeh6").text
                                # chars = find_characteristics(descrs)
                                chars = chat_get_chars(title, f'{descrs} {chs}')
                                print('chs', chs)
                            except:
                                chars = chat_get_chars(title, descrs)

                            print('chars', chars)
                        except:
                            chars = {}

                        if not chars:
                            chars = {}

                        time.sleep(8)
                        if img:
                            pic_name = download_pic(f'{img}')
                        else:
                            pic_name = 'Н.Д.'

                        if ok:
                            price = await sync_to_async(price_validator)(price)
                            await sync_to_async(update_exist_prod_pars)({'name': title,
                                                                         'type_': chat_get_type(title, f'{chs}'),
                                                                         'price': price, 'available': status, 'chars': chars},
                                                                        url=u)
                            continue

                        await run_add_prod_from_sites([title, price, chars, pic_name, descrs], url=u, req=req, status=status)
def registaration(name, email, passw):
    hash_object = hashlib.sha256()
    hash_object.update(passw.encode('utf-8'))
    hash_pass = hash_object.hexdigest()
    if User_my.objects.filter(email=email).count() > 0:
        return None
    u = User_my.objects.create(name=name, email=email, pass_hash=hash_pass)
    u.save()
    return u


def is_true_password(passw, email):
    user = User_my.objects.filter(email=email).first()  # Получаем объект пользователя из базы данных
    if user is not None:
        true_hash = user.pass_hash
        # Хешируем незашифрованный пароль
        hash_object = hashlib.sha256()
        hash_object.update(passw.encode('utf-8'))
        hashed_pass = hash_object.hexdigest()
        # Сравниваем хэши
        if hashed_pass == true_hash:
            return True
    return False





def bd_tables_names():
    tables = connection.introspection.table_names()
    selected_tables = [table for table in tables if table.startswith('cat_') and not table.endswith('my')]
    all_names = []
    for table in selected_tables:
        all_names.append(table)
    return all_names


async def async_update(model, dictt, title):
    line = await sync_to_async(model.objects.get)(id=title)
    for key, value in dictt.items():
        if hasattr(line, key):
            field = getattr(model, key)
            if isinstance(field, FloatField):
                try:
                    value = price_validator(value)  # Преобразуем значение в int
                except:
                    continue
            elif isinstance(field, IntegerField):
                try:
                    value = int(price_validator(value))  # Преобразуем значение в int
                except:
                    continue

            elif isinstance(field, BooleanField):
                if value.find('нет') != -1 or value.find('без') != -1:
                    value = False
                else:
                    value = True

            setattr(line, key, value)
    await sync_to_async(line.save)()

# async def async_update(model, dictt, title):
#     line = await sync_to_async(model.objects.get)(id=title)
#     for key, value in dictt.items():
#         setattr(line, key, value)
#     await sync_to_async(line.save)()


def transfer_record(source_model, target_model, record_id):
    # Получение исходной записи
    source_record = source_model.objects.get(id=record_id)
    # Создание экземпляра целевой модели
    target_record = target_model()

    # Копирование значений совпадающих полей
    for field in source_model._meta.fields:
        if hasattr(target_model, field.name):
            value = getattr(source_record, field.name)
            setattr(target_record, field.name, value)

    # Сохранение целевой записи
    target_record.save()
    un = UniqIdProds.objects.filter(native_id=record_id, model=str(source_model.__name__).lower()).first()
    un.native_id = target_record.id
    un.model = target_record.__class__.__name__
    un.save()

    # Удалить старую запись
    source_record.delete()

def transfer_record_unk(target_model, record_id):
    source_record = UnknownType.objects.get(id=record_id)
    target_record = target_model()

    # Перенос значения 'name'
    target_record.name = source_record.name

    # Разворачивание поля 'datas' в виде словаря
    datas = source_record.datas
    if isinstance(datas, str):
        datas = re.sub(r'(\w+)(?=\s*:)', r"'\1'", datas)
        datas = ast.literal_eval(datas)

    for key, value in datas.items():
        try:
            field = target_model._meta.get_field(key)
        except:
            continue
        if isinstance(field, models.BooleanField):
            if value:
                value = True
            else:
                value = False
        elif isinstance(field, models.IntegerField):
            value = int(re.sub(r"\D", "", value))

        elif isinstance(field, models.FloatField):
            value = price_validator(str(value))

        target_record.__dict__[key] = value

    # Сохранение целевой записи
    target_record.save()

    # Удаление исходной записи
    source_record.delete()




def not_second_columns(fields):
    bad_words = ['name', 'pic', 'full_desc', 'draft_chars', 'descr', 'full_desc', 'datas']
    good_words = []
    for field in fields:
        if field not in bad_words:
            good_words.append(field)
    return good_words



def do_note_history(user_id, title=None, a_dict=None, addit_opt=None, olds=None):
    user = User_my.objects.get(id=user_id)
    done = {}
    obj = None

    if title:
        for model in apps.get_models():
            if any(isinstance(field, models.CharField) and field.name == 'name' for field in model._meta.get_fields()):
                obj = model.objects.filter(name__icontains=title).first()
                if obj:
                    break

        if not obj and olds:
            model = olds['модель']
            obj = model.objects.filter(id=olds['id']).first()


        if a_dict and obj:
            for k, v in a_dict.items():
                try:
                    if getattr(obj, k) != v and v != 'None':
                        done[k] = f'было изменено значение с {getattr(obj, k)} на {v}'
                except:
                    continue


        if addit_opt:
            done['тип'] = addit_opt

        if done:
            done['товар'] = title
            History.objects.create(i_c=user.name, done=done, date_of_change=datetime.today(), title_prod=title)
    else:
        done = {'Сделано': ' Удаление всех неизвестных по-типу товаров'}
        History.objects.create(i_c=user.name, done=done, date_of_change=datetime.today(), title_prod='Н.Д.')


def is_admin(req):
    id_user = req.session.get('_auth_user_id', None)
    if id_user:
        user = User_my.objects.get(id=int(id_user))
        stat = user.status
        if stat != 'Клиент':
            return True
    return False

async def async_is_admin(req):
    id_user = await sync_to_async(req.session.get)('_auth_user_id', None)
    if id_user:
        user = await sync_to_async(User_my.objects.get)(id=int(id_user))
        stat = user.status
        if stat != 'Клиент':
            return True
    return False

def get_users():
    super_ = User_my.objects.filter(status='Супер')
    admins = User_my.objects.filter(status='Админ')
    users = User_my.objects.filter(status='Клиент')
    return super_, admins, users

def is_super(req):
    id = req.session.get('_auth_user_id', None)
    if id:
        try:
            user = User_my.objects.get(id=id)
        except:
            return False
        if user.status == 'Супер':
            return True
        else:
            return False
    return False

async def async_is_super(req):
    id = await sync_to_async(req.session.get)('_auth_user_id', None)
    user = await sync_to_async(User_my.objects.get)(id=id)
    if user.status == 'Супер':
        return True
    else:
        return False

def get_models_and_carac():
    models = []
    caracts = set()
    all_models = apps.get_models()

    for model in all_models:
        if model.__name__ not in ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'UnknownType',
                                  'User_my', 'History', 'UniqIdProds']:
            fields = [field.name for field in model._meta.fields]
            models.append(model.__name__)
            for f in fields:
                caracts.add(f)

    for c in ['programs', 'descr', 'full_desc', 'draft_chars', 'name', 'descr', 'pic', 'type_of_prod', 'available', 'id']:
        try:
            caracts.remove(c)
        except:
            pass

    return models, caracts

def trans_models_carac(chars=None, reverse=False):
    # Если reverse то с англ на рус
    new_chars = dict()

    if reverse: # Получить русские знчаения
        models = d.values()
        caracts = dict()
        for k, v in c.items():
            if type(v) == type(caracts):
                caracts[k] = 'bool'
            else:
                caracts[k] = 'not'

        return models, caracts


    elif not reverse: # На английский chars
        for k, v in chars.items():
            if k in ['yes', 'no', 'four']:
                new_chars[k] = v
            elif k.lower() in c.keys(): # Перевод на англ характеристик
                new_chars[str(c[k.lower()])] = v

        try:
            if chars['categ']:
                for k, v in d.items():
                    if chars['categ'].lower() == v.lower(): # Перевод на англ модели
                        new_chars['categ'] = k.lower()
        except:
            pass

        return new_chars

def update_chars_translate(chars, eng=None, rus=None):
    if rus:
        cc = {**chars}
        charss = dict()
        for k, v in cc.items():
            for kk, vv in c.items():
                if isinstance(vv, dict):
                    vv = next(iter(vv))

                if k == vv:
                    print(vv, k)
                    charss[kk] = v

        return charss
    else:
        cc = {**chars}
        charss = dict()
        for k, v in cc.items():
            k = k.replace('update_', '')
            if isinstance(c[k], dict):
                a = next(iter(c[k]))
                charss[a] = v
            else:
                charss[c[k]] = v

        return charss

def dict_out(dic):
    d = {}
    if type(dic) == type(''):
        try:
            dic = ast.literal_eval(dic)
        except:
            dic = json.loads(dic)
    for k, v in dic.items():
        if type(v) == type(d):
            d = {**d, **v}
        else:
            d = {**d, k: v}
    return d

def chat_get_chars(title, descr, model="gpt-3.5-turbo-16k"):
    if len(descr) > 600:
        descr = descr[:600]
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer key"
    }

    type_ = chat_get_type(title, descr)
    # Здесь получаем какие именно характеристики нам нужны
    fields = get_exactly_chars(type_)
    print(fields)

    data = {
        # "model": "gpt-3.5-turbo",
        # "model": "gpt-3.5-turbo-16k",
        # "model": "gpt-3.5-turbo-0613",
        "model": model,
        "messages": [
            {"role": "system", "content": f"""Мне нужно чтобы ты нашел эти характеристики ({fields})в тексте и записал их в виде словаря питона и больше ничего не писал кроме словаря, где ключ на английском и слова в ключе должны быть точь в точь такими же как я написал, а значение на русском языке какие найдешь в этом тексте, и еслт не найдешь значение то напищи в значение Н.Д.:
    {descr}"""},
            {"role": "user", "content": descr}
        ]
    }

    response = requests.post(URLL, headers=headers, json=data)
    result = response.json()
    print(response)
    try:
        result = result['choices'][0]['message']['content']
    except:
        time.sleep(27)
        try:
            response = requests.post(URLL, headers=headers, json=data)
            result = response.json()
            result = result['choices'][0]['message']['content']
        except:
            try:
                return chat_get_chars(title, descr, model="gpt-3.5-turbo")
            except:
                return chat_get_chars(title, descr, model="gpt-3.5-turbo-0613")

    try:
        result = ast.literal_eval(result)
    except:
        try:
            result = json.loads(result)
        except:
            return chat_get_chars(title, descr)
    dd = dict_out(result)
    print('DICKKKK', dd)
    return dd


def get_exactly_chars(type_):
    model = apps.get_model(app_label='cat', model_name=type_)
    fields = model._meta.get_fields()
    field_names = [field.name for field in fields]
    true_f = []
    for f in field_names:
        if not (f in ['id', 'name', 'type_of_prod', 'descr', 'pic', 'full_desc', 'price', 'price_opt', 'draft_chars', 'url', 'art', 'available']):
            true_f.append(f)

    return true_f
