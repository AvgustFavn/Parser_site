import os
import time
from asyncio.log import logger
import asyncio

import requests
from asgiref.sync import sync_to_async, async_to_sync
from django.apps import apps
from django.db import connections, connection
from django.db.models import QuerySet, CharField, Q, IntegerField, BooleanField
from openpyxl.reader.excel import load_workbook
import pandas as pd

from cat.find_caract import find_characteristics
from cat.models import *
from cat.parsing_back import change_pic

URLL = "https://api.openai.com/v1/chat/completions"
chat_value = 0

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

def pars_type_prod(title, descr):
    for typ in types:
        if str(typ).lower() in str(title).lower() or str(typ).lower() in str(descr).lower():
            return typ
    return None


async def add_prod_from_sites(sites_datas=None, chars_p=None, req=None, url=None, datas=None, status=None):
    obj = None
    if datas:
        logger.debug('Начинается добавление продукта')
        name = datas[0]
        print(f'TOBAP {name}')
        price = price_validator(datas[1])
        # typ = pars_type_prod(datas[0], datas[-1])
        chars = datas[2]
        if len(chars) < 1:
            chars = {}
        full_descr = datas[-1]
        if not full_descr:
            full_descr = 'Н.Д.'
        elif len(full_descr) > 449:
            full_descr = full_descr[:449]
        pic = datas[-2]
        if chars_p:
            a = add_forms_chars(chars_p)
        else:
            a = {}
        aa = {'descr': full_descr, 'name': name, 'price': price, 'url': url,
             'pic': pic, 'available': status}

        if a:
            aa.update(a)
        # if chars:
        #     # Переимененный ключами словарь
        #     chars = good_keys_for_chars(chars)
        #     aa.update(chars)

        a = aa
        typ = chat_get_type(name, f'{full_descr} {chars}')
        print('Создаем новое')
    else:
        name = chars_p['name']
        if name == None:
            return None


        chars = chars_p['chars']
        # del_k = []
        # ch = {}
        # for k, v in chars.items():
        #     translate = arg_for_bd(k)
        #     if translate:
        #         ch[translate] = v
        #         del_k.append(k)
        #
        # chars = {**chars, **ch}
        # for d in del_k:
        #     chars.pop(d)


        a = chars
        max_ = chars_p['max_']
        min_ = chars_p['min_']
        a['art'] = chars_p.get('art', 'Н.Д.')
        a['name'] = name
        if len(name) > 199:
            a['name'] = name[:199]
        edge = chars_p['edge']
        price = max_
        price_opt = min_
        full_descr = f"""{chars_p['descr']}
        Данные из файла - осталось {edge}, артикул {a["art"]}"""


        if price != 'Н.Д.':
            a['price'] = price
        else:
            a['price'] = None

        if price_opt != 'Н.Д.':
            a['price_opt'] = price_opt
        else:
            a['price_opt'] = None

        a['descr'] = full_descr
        a['url'] = url
        a['available'] = chars_p['available']
        idd = a.get('id', None)
        if idd:
            del a['id']

        typ = chat_get_type(name, f'{full_descr} {chars}')
        print('Узнали тип при создании товара ', typ)
        print('Создаем новое')


    if not typ:
        dic = {**a}
        try:
            await sync_to_async(UnknownType.objects.create)(name=name, datas=dic)
        except:
            return None


    elif typ == 'SportsThings':
        fields = [field.name for field in SportsThings._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        print(a)
        obj = await sync_to_async(SportsThings.objects.create)(**{
            **a
        })

    elif typ == 'MusicAccessories':
        fields = [field.name for field in MusicAccessories._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        obj = await sync_to_async(MusicAccessories.objects.create)(**a)


    elif typ == 'Clothes':
        fields = [field.name for field in Clothes._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        obj = await sync_to_async(Clothes.objects.create)(**{
            **a
        })

    elif typ == 'Headset':
        fields = [field.name for field in Headset._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        obj = await sync_to_async(Headset.objects.create)(**{
            **a
        })

    elif typ == 'Speakers':
        fields = [field.name for field in Speakers._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        obj = await sync_to_async(Speakers.objects.create)(**{
            **a
        })

    elif typ == 'Microphone':
        fields = [field.name for field in Microphone._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        obj = await sync_to_async(Microphone.objects.create)(**{
            **a
        })

    elif typ == 'StringedInstruments':
        fields = [field.name for field in StringedInstruments._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        obj = await sync_to_async(StringedInstruments.objects.create)(**{
            **a
        })

    elif typ == 'KeyboardInstruments':
        fields = [field.name for field in KeyboardInstruments._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        obj = await sync_to_async(KeyboardInstruments.objects.create)(**{
            **a
        })

    elif typ == 'WindInstruments':
        fields = [field.name for field in WindInstruments._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        obj = await sync_to_async(WindInstruments.objects.create)(**{
            **a
        })

    elif typ == 'PercussionInstruments':
        fields = [field.name for field in PercussionInstruments._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        obj = await sync_to_async(PercussionInstruments.objects.create)(**{
            **a
        })

    elif typ == 'Accordion':
        fields = [field.name for field in Accordion._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        obj = await sync_to_async(Accordion.objects.create)(**{
            **a
        })


    elif typ == 'StoveAndOven':
        fields = [field.name for field in StoveAndOven._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        obj = await sync_to_async(StoveAndOven.objects.create)(**{
            **a
        })

    elif typ == 'Fridges':
        fields = [field.name for field in Fridges._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Fridges.objects.create)(**{
                **a
            })

    elif typ == 'Dishwashers':
        fields = [field.name for field in Dishwashers._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Dishwashers.objects.create)(**{
                **a
            })


    elif typ == 'ForDrinks':
        fields = [field.name for field in ForDrinks._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(ForDrinks.objects.create)(**{
                **a
            })

    elif typ == 'Grills':
        fields = [field.name for field in Grills._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Grills.objects.create)(**{
                **a
            })


    elif typ == 'Toasters':
        fields = [field.name for field in Toasters._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Toasters.objects.create)(**{
                **a
            })


    elif typ == 'Fryers':
        fields = [field.name for field in Fryers._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Fryers.objects.create)(**{
                **a
            })


    elif typ == 'KitchenScales':
        fields = [field.name for field in KitchenScales._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(KitchenScales.objects.create)(**{
                **a
            })


    elif typ == 'Multicookers':
        fields = [field.name for field in Multicookers._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Multicookers.objects.create)(**{
                **a
            })


    elif typ == 'WashingMachines':
        fields = [field.name for field in WashingMachines._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(WashingMachines.objects.create)(**{
                **a
            })

    elif typ == 'Dryer':
        fields = [field.name for field in Dryer._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Dryer.objects.create)(**{
                **a
            })

    elif typ == 'Irons':
        fields = [field.name for field in Irons._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Irons.objects.create)(**{
                **a
            })


    elif typ == 'RobotVacuumCleaner':
        fields = [field.name for field in RobotVacuumCleaner._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(RobotVacuumCleaner.objects.create)(**{
                **a
            })

    elif typ == 'VacuumCleaners':
        fields = [field.name for field in VacuumCleaners._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(VacuumCleaners.objects.create)(**{
                **a
            })

    elif typ == 'WaterHeaters':
        fields = [field.name for field in WaterHeaters._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(WaterHeaters.objects.create)(**{
                **a
            })

    elif typ == 'AirConditioners':
        fields = [field.name for field in AirConditioners._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(AirConditioners.objects.create)(**{
                **a
            })

    elif typ == 'Heaters':
        fields = [field.name for field in Heaters._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Heaters.objects.create)(**{
                **a
            })


    elif typ == 'Fans':
        if a:
            fields = [field.name for field in Fans._meta.get_fields()]
            filtered_fields = {key: value for key, value in a.items() if key in fields}
            a = filtered_fields
            obj = await sync_to_async(Fans.objects.create)(**{
                **a
            })


    elif typ == 'Sewing':
        fields = [field.name for field in Sewing._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Sewing.objects.create)(**{
                **a
            })

    elif typ == 'HairStylingDrying':
        fields = [field.name for field in HairStylingDrying._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(HairStylingDrying.objects.create)(**{
                **a
            })

    elif typ == 'ElectricShavers':
        fields = [field.name for field in ElectricShavers._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(ElectricShavers.objects.create)(**{
                **a
            })

    elif typ == 'PhotoEquipment':
        fields = [field.name for field in PhotoEquipment._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(PhotoEquipment.objects.create)(**{
                **a
            })

    elif typ == 'Microwave':
        fields = [field.name for field in Microwave._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Microwave.objects.create)(**{
                **a
            })

    elif typ == 'Lighting':
        fields = [field.name for field in Lighting._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Lighting.objects.create)(**{
                **a
            })

    elif typ == 'Sockets':
        fields = [field.name for field in Sockets._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Sockets.objects.create)(**{
                **a
            })

    elif typ == 'Printers':
        fields = [field.name for field in Printers._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Printers.objects.create)(**{
                **a
            })

    elif typ == 'BoardGames':
        fields = [field.name for field in BoardGames._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(BoardGames.objects.create)(**{
                **a
            })

    elif typ == 'ChildToys':
        fields = [field.name for field in ChildToys._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(ChildToys.objects.create)(**{
                **a
            })

    elif typ == 'Wires':
        fields = [field.name for field in Wires._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Wires.objects.create)(**{
                **a
            })

    elif typ == 'Routers':
        fields = [field.name for field in Routers._meta.get_fields()]
        filtered_fields = {key: value for key, value in a.items() if key in fields}
        a = filtered_fields
        if a:
            obj = await sync_to_async(Routers.objects.create)({
                **a
            })
    else:
        dic = {**a}
        try:
            obj = await sync_to_async(UnknownType.objects.create)(name=name, datas=dic)
        except:
            return None

    if obj:
        print(f'Создали {obj.name}')
        model = (obj.__class__.__name__).lower()
        await sync_to_async(UniqIdProds.objects.create)(
            native_id=obj.id,
            model=model
        )


def add_forms_chars(chars):
    atrs = dict()
    for k, v in chars.items():
        translate = arg_for_bd(k)
        if translate:
            atrs[translate] = v

    atrs = clear_dict(atrs)
    if atrs:
        return atrs
    else:
        return None


def arg_for_bd(word):
    for k, v in c.items():
        if word in k or k in word:
            if type(v) == type(''):
                return v
            elif type(v) == type({'1': '2'}):
                return list(v.keys())[0]


def clear_dict(dictionary):
    keys_to_remove = []
    for key, values in dictionary.items():
        if key == 'csrfmiddlewaretoken' or key == 'email':
            keys_to_remove.append(key)

        non_empty_values = [value for value in values if value.strip() != '']
        if non_empty_values:
            dictionary[key] = non_empty_values
        else:
            keys_to_remove.append(key)

    for key in keys_to_remove:
        dictionary.pop(key, None)

    return dictionary


def chars_of_types():
    d = {
        'all': ['производитель', 'цвет', 'материал', 'максимальная потребляемая мощность',
                'напряжение питания', 'вес', 'цена', 'класс энергопотребления', 'доп. название товара'],
        'печь / духовка': ['объем печи', 'максимальная температура'],
        'холодильник': ['объем', 'минимальная температура', 'уровень шума', 'хладагент', ],
        'посудомойка': ['объем', 'минимальная температура', 'материал', 'тип сушки', 'максимальная температура',
                        'потребление воды', 'потребление энергии'],
        'апараты для напитков': ['объем', 'тип нагревательного элемента', 'максимальная температура',
                                 {'поддержание температуры': 'bool'}, ],
        'гриль': ['минимальная температура', 'максимальная температура', {'регулировка термостата': 'bool'},
                  'рабочая поверхность', ],
        'тостер': ['максимальная температура', 'количество отделений', 'количество тостов',
                   {'автоотключение': 'bool'}, {'трафарет': 'bool'}],
        'фритюр': ['минимальная температура', 'максимальная температура', 'объем', {'автослив масла': 'bool'}],
        'мультиварка': ['максимальная температура', 'минимальная температура', 'объем',
                        {'поддержание температуры': 'bool'}],
        'кухонные весы/ весы': ['лимит веса', 'точность взвешивания', 'тип батареи', ],
        'стиралка': ['объем', 'максимальный вес', 'минимальная температура', 'максимальная температура', 'уровень шума',
                     'потребление воды', 'скорость вращения барабана'],
        'сушилка': ['объем', 'максимальный вес', 'уровень шума', ],
        'утюг': ['максимальная температура', 'минимальная температура', ],
        'пылесос': ['тип уборки', 'уровень шума', {'регулятор мощности': 'bool'}],
        'робот пылесос': ['тип уборки', 'уровень шума', 'тип сенсоров', 'время работы', 'время зарядки'],
        'водонагреватель/ бойлер': ['минимальная температура', 'максимальная температура', 'объем', 'способ крепления',
                                    'расход топлива'],
        'кондиционер': ['мощность охлаждения', 'мощность обогрева', 'отапливаемая территория', 'хладагент', ],
        'вентилятор': ['способ крепления', {'регулятор мощности': 'bool'}, {'регулировка термостата': 'bool'},
                       'рабочая территория'],
        'обогреватель': ['способ крепления', 'топливо', 'расход топлива', {'регулятор мощности': 'bool'},
                         {'регулировка термостата': 'bool'}, 'отапливаемая территория', ],
        'швейная машинка': ['тип челнока', {'регулировка скорости шитья': 'bool'}, {'двойная игла': 'bool'}, ],
        'уход за волосами': [{'защита от перегрева': 'bool'}, 'насадки', 'максимальная температура'],
        'электро-бритва': ['насадки', {'cамозатачивающиеся ножи': 'bool'}, 'материал лезвий', 'время зарядки'],
        'фотоаппараты и их комплектация': ['общее число мегапикселей матрицы', 'число эффективных мегапикселей',
                                           'тип матрицы', 'максимальное разрешение', 'количество объективов',
                                           {'поддержка 4К': 'bool'}, {'поддержка full hd': 'bool'}, ],
        'микроволновка': ['объем', 'рабочая поверхность'],
        'свет': ['цокль', 'цвет света', 'срок службы', 'колличество источников света',
                 'максимальная освещаемая территория', ],
        'розетка/ переключатель': ['внутренние габариты', 'колличество кнопок', ],
        'принтеры/ сканеры': ['скорость печати', 'технология подключения', {'двусторонняя печать': 'bool'},
                              'поддерживаемые форматы бумаг',
                              {'цветная печать': 'bool'}, ],
        'настольные игры': ['издательский дом', 'кол-во игроков', 'время игры', 'ограничения по возрасту', 'жанр',
                            'язык игры', ],
        'детские игрушки': ['материал на ощупь', 'вес', 'цвет'],
        'провода': ['проводник', 'изоляция', 'электрическое сопротивление', 'рабочее напряжение'],
        'роутер/ маршрутизатор': ['стандарт wifi', 'максимальная скорость', ],
        'струнные музыкальные инструменты': ['колки', 'мензура', 'звукосниматель', 'размер в четвертях', ],
        'наушники': ['минимальная воспроизводимая частота', 'максимальная воспроизводимая частота', 'сопротивление',
                     'чувствительность', {'микрофон': 'bool'}, 'время работы', 'время зарядки'],
        'колонки': ['минимальная воспроизводимая частота', 'максимальная воспроизводимая частота', 'мощность',
                    'время работы',
                    'время зарядки', {'поддержка карты памяти': 'bool'}, ],
        'микрофон': ['принцип работы', 'сопротивление', 'чувствительность', 'способ передачи сигнала', ],
        'клавишные музыкальные инструменты': ['колличество кнопок', 'мощность', 'гнезда', 'тембр'],
        'духовые музыкальные инструменты': ['строй', 'части', 'размер в четвертях', ],
        'ударные музыкальные инструменты': ['пэд', 'гнезда', ],
        'аккордеон /гармони': ['правая рука', 'левая рука', 'регистры', 'ряды', 'размер в четвертях', ],

    }
    return d


def get_alalogs(word):
    d = chars_of_types()

    for k, v in d.items():
        if word in k or k in word:
            new_list = [x for x in v if not isinstance(x, dict)]
            return new_list
        elif word in v:
            new_list = [x for x in v if not isinstance(x, dict)]
            return new_list

    return None


types = ['печь', 'духовка', 'плита', 'духовой шкаф', 'конфорка', 'комфорка', 'холодильник', 'морозилка', 'посудомойка',
         'посудомоечная',
         'электрочайник', 'чайник', 'термопот', 'чай-машина', 'чай машина', 'кофемашин', 'кофеварка', 'кофемолка',
         'самовар', 'соковыжималка', 'соко-выжималка', 'гриль', 'аэрогриль', 'сэндвичница', 'вафельница', 'тостер',
         'шашлычница',
         'мультиварка', 'скороварка',
         'фритюрница', 'фритюр', 'кухонные весы', 'электро весы', 'весы', 'стиральная машина', 'стиралка',
         'бельевая машина', 'сушилка', 'сушильная машина', 'утюг', 'пылесос', 'пылесосный аппарат',
         'робот пылесос', 'робот-пылесос', 'автопылесос', 'водонагреватель', 'бойлер', 'котел', 'кондиционер',
         'вентилятор', 'обогреватель', 'тепловентелятор',
         'швейная машин', 'оверлок', 'фен', 'щипцы для', 'выпрямитель для', 'мультистайлер', 'бритва', 'триммер',
         'машинка для волос', 'машинка для стрижки волос', 'электробритва', 'эпилятор',
         'фотоэпилятор', 'фотоаппарат', 'экшн-камера', 'экшн камера', 'экшнкамера', 'камера', 'объектив', 'обьектив',
         'штатив', 'стабилизатор', 'микроволновка', 'микроволновая печь', 'микроволн',
         'светильник', 'лампа', 'лампочка', 'люстра', 'софит', 'светодиодные', 'бра', 'спот', 'фонарь', 'фонарик',
         'ночник', 'светодиодная', 'выключатель', 'розетка', 'переключатель', 'принтер', 'мфу', 'сканнер', 'сканер',
         'настольная игра', 'настолка', 'детская игрушка', 'игрушка', 'для детей', 'провод', 'кабель', 'разъем',
         'роутер', 'маршрутизатор', 'наушники', 'гарнитура', 'вкладыши', 'акустика', 'сабвуфер', 'колонки', 'колонка',
         'магнитола',
         'микрофон', 'спикерфон', 'струнн', 'скрипка', 'гитара', 'укулеле', 'альт', 'виолончель', 'контрабас',
         'синтезатор', 'пианино',
         'орган', 'фортепиано', 'рояль', 'блокфлейта', 'флейта', 'саксофон', 'кларнет', 'труба', 'тромбон', 'туба',
         'гобой', 'фагот',
         'флюгельгорн', 'корнет', 'валторна', 'альтгорн', 'теноргорн', 'баритон', 'эуфониум', 'ударные', 'перкуссия',
         'аккордеон', 'баян', 'гармони',       'струны', 'нот', 'нотн', 'смычок', 'смыч', 'чехол', 'усилитель', 'тюнер',
         'метроном', 'медиатор', 'палочки', 'педал', 'мяч', 'ракетка', 'волан', 'секундомер', 'таймер', 'гантел',
         'гиря', 'сетка', 'бассейн', 'бодибар', 'булава', 'бокс', 'кольцо', 'лента', 'обруч', 'турник', 'эспандер',
         'хокке', 'баскетбо', 'скакалка', 'футбол', 'перчатки', 'форма', 'гетры', 'нарукавники', 'футболка', 'майка',
         'жилет', 'ласты', 'маска', 'рейтузы', 'капа', 'наколенники', 'кимоно', 'куртка', 'пояс', 'напульсник', 'браслет',
        'беруши', 'полотенце', 'плав', 'рюкзак', 'сумка', 'шапка', 'купальный костюм', 'плавки', 'купальник', 'очки',
         'шарф', 'ботинки', 'обувь', 'шорты', 'штаны', 'брюки', 'носки', 'гольфы', 'кофта', 'свитер', 'сланцы', 'наколенники',
         ]



def update_exist_prod_file(chars_p, url):
    name = chars_p['name']
    if name == None:
        return None

    chars = chars_p['chars']
    del_k = []
    ch = {}
    for k, v in chars.items():
        translate = arg_for_bd(k)
        if translate:
            ch[translate] = v
            del_k.append(k)

    chars = {**ch}
    print('Перведенный чарс ', chars)
    # for d in del_k:
    #     chars.pop(d)

    typ = chars_p['type_']
    print(typ)

    a = chars
    max_ = chars_p['max_']
    min_ = chars_p['min_']
    descr = chars_p['descr']
    a['art'] = chars_p.get('art', 'Н.Д.')
    edge = chars_p['edge']
    a['type_of_prod'] = typ
    if max_ != 'Н.Д.':
        a['price'] = max_
    else:
        a['price'] = None

    if min_ != 'Н.Д.':
        a['price_opt'] = min_
    else:
        a['price_opt'] = None

    full_descr = f"""{descr}
    Данные из файла - осталось {edge}, артикул {a["art"]}"""

    a['descr'] = full_descr
    a['url'] = url
    a['available'] = chars_p['available']
    rows = get_all_prods()
    unks = get_all_unk_prods()
    for row in rows:
        if len(name) > 199:
            titl = name.lower()[:199]
        else:
            titl = name.lower()
        if titl in row['name'].lower():
            if titl and len(titl) > 2:
                line = row
                id_line = line['global_id']
                obj = find_prod_glob(id_line)
                print(obj)
                if obj:
                    model_fields = obj._meta.get_fields()
                    for key, value in a.items():
                        if key in [field.name for field in model_fields]:
                            setattr(obj, key, value)

                    obj.save()
                else:
                    return None


    for row in unks:
        if len(name) > 199:
            titl = name.lower()[:199]
        else:
            titl = name.lower()
        if titl in row['name'].lower():
            if titl and len(titl) > 2:
                line = row
                obj = UnknownType.objects.get(id=line['id'])
                if obj:
                    obj.datas = a
                    obj.save()


def update_exist_prod_pars(chars_p, url):
    name = chars_p['name']
    charss = chars_p['chars']
    print(name)
    if name == None:
        return None

    # if charss:
    #     # Переимененный ключами словарь
    #     charss = good_keys_for_chars(charss)

    # ch = {}
    # for k, v in charss.items():
    #     translate = arg_for_bd(k)
    #     if translate:
    #         ch[translate] = v

    # chars = {**ch}
    chars = {**charss}
    chars['url'] = url
    chars['price'] = chars_p['price']
    chars['available'] = chars_p['available']
    rows = get_all_prods()
    unks = get_all_unk_prods()
    for row in rows:
        if len(name) > 199:
            titl = name.lower()[:199]
        else:
            titl = name.lower()
        if titl in row['name'].lower():
            if titl and len(titl) > 2:
                line = row
                id_line = line['global_id']
                obj = find_prod_glob(id_line)
                if obj:
                    change_pic(obj.pic)
                    model_fields = obj._meta.get_fields()
                    print(f'Апдейт поля которые есть в моделе: {model_fields}')
                    print('Типы', chars_p['type_'], obj.__class__.__name__)
                    if chars_p['type_'] != obj.__class__.__name__:
                        try:
                            obj_name = obj.name
                            to_model = find_model(chars_p['type_'])
                            transfer_record(find_model(obj.__class__.__name__), to_model, obj.id)
                            print('Сменили модель')
                            obj = to_model.objects.filter(name=obj_name).first()
                            for key, value in chars.items():
                                if key in [field.name for field in model_fields] and value:
                                    try:
                                        field = obj._meta.get_field(key)
                                    except:
                                        continue
                                    if isinstance(field, CharField) and len(
                                            value) > field.max_length:  # Проверяем тип и длину значения
                                        value = value[:field.max_length]  # Обрезаем значение до максимальной длины поля

                                    elif isinstance(field, IntegerField) and type(value) != type(2):
                                        continue
                                    elif isinstance(field, BooleanField) and type(value) != type(2.0):
                                        continue

                                    setattr(obj, key, value)
                            print('Сменили характеристики')
                            obj.save()
                            return None
                        except:
                            print('Без смены модели')
                            for key, value in chars.items():
                                if key in [field.name for field in model_fields] and value:
                                    try:
                                        field = obj._meta.get_field(key)
                                    except:
                                        continue
                                    if isinstance(field, CharField) and len(
                                            value) > field.max_length:  # Проверяем тип и длину значения
                                        value = value[:field.max_length]  # Обрезаем значение до максимальной длины поля
                                    elif isinstance(field, IntegerField) and type(value) != type(2):
                                        continue
                                    elif isinstance(field, BooleanField) and type(value) != type(2.0):
                                        continue
                                    setattr(obj, key, value)
                            obj.save()
                            return None
                    else:
                        for key, value in chars.items():
                            if key in [field.name for field in model_fields] and value:
                                try:
                                    field = obj._meta.get_field(key)
                                except:
                                    continue
                                if isinstance(field, CharField) and len(
                                        value) > field.max_length:  # Проверяем тип и длину значения
                                    value = value[:field.max_length]  # Обрезаем значение до максимальной длины поля
                                elif isinstance(field, IntegerField) and type(value) != type(2):
                                    continue
                                    
                                elif isinstance(field, BooleanField) and type(value) != type(2.0):
                                    continue

                                setattr(obj, key, value)

                        print('Обновили')
                        obj.save()
                        return None
                else:
                    return None


    for row in unks:
        if len(name) > 199:
            titl = name.lower()[:199]
        else:
            titl = name.lower()
        if titl in row['name'].lower():
            if titl and len(titl) > 2:
                line = row
                obj = UnknownType.objects.get(id=line['id'])
                if obj:
                    if chars_p['type_'] != obj.__class__.__name__:
                        obj_name = obj.name
                        to_model = find_model(chars_p['type_'])
                        transfer_record(find_model(obj.__class__.__name__), to_model, obj.id)
                        print(f'Сменили модель с Неизвестных на {to_model}')
                        obj = to_model.objects.filter(name=obj_name).first()
                        model_fields = obj._meta.get_fields()
                        for key, value in chars.items():
                            if key in [field.name for field in model_fields] and value:
                                try:
                                    field = obj._meta.get_field(key)
                                except:
                                    continue
                                if isinstance(field, CharField) and len(
                                        value) > field.max_length:  # Проверяем тип и длину значения
                                    value = value[:field.max_length]  # Обрезаем значение до максимальной длины поля
                                setattr(obj, key, value)
                        print('Сменили характеристики')
                        obj.save()
                        return None

                    else:
                        pic = dict(obj.datas).get('pic', None)
                        if pic:
                            change_pic(pic)
                        obj.available = chars['available']
                        obj.datas = chars
                        obj.save()
                        print('Обновили')



def find_prod_glob(id):
    try:
        line = UniqIdProds.objects.get(id=id)
    except:
        return None

    model = find_model(line.model)
    id_prod = line.native_id
    print(id_prod)
    try:
        obj = model.objects.get(id=id_prod)
    except:
        return None
    return obj


def find_model(table_name):
    app_label = 'cat'
    app_config = apps.get_app_config(app_label)
    models = app_config.get_models()

    if 'cat' in table_name:
        ModelClass = None
        for model in models:
            if model._meta.db_table == table_name:
                ModelClass = model
                return ModelClass
    else:
        for model in models:
            if model._meta.db_table.lower() == f'{app_label}_{table_name}'.lower():
                return model
            elif model.__name__.lower() in f'{table_name}'.lower():
                return model

def pars_file_chars(name):
    chars = find_characteristics(name)
    return chars


async def unique_prods(title):
    rows = await sync_to_async(get_all_prods)()
    unks = await sync_to_async(get_all_unk_prods)()
    for row in rows:
        if len(title) > 199:
            titl = title.lower()[:199]
        else:
            titl = title.lower()
        if titl in row['name'].lower():
            return True

    for row in unks:
        if len(title) > 199:
            titl = title.lower()[:199]
        else:
            titl = title.lower()
        if titl in row['name'].lower():
            return True

    return False


def get_all_unk_prods():
    lines = UnknownType.objects.all().order_by('-id').values()
    return list(lines)


def get_all_prods():
    tables = connection.introspection.table_names()
    selected_tables = [table for table in tables if
                       table.startswith('cat_') and not table.endswith('my') and not table.startswith('cat_unk') and not table.startswith('cat_hist') and not table.startswith('cat_uniq') and not table.startswith('cat_providers')]
    all_lines = []
    for table in selected_tables:
        with connections['default'].cursor() as cursor:
            cursor.execute("SELECT * FROM {}".format(table))
            rows = cursor.fetchall()
            if rows:
                columns = [col[0] for col in cursor.description]
                table_lines = [dict(zip(columns, row)) for row in rows]
                for t in table_lines:
                    t['table'] = table
                all_lines.extend(table_lines)  # Здесь исправление

    for r in all_lines:
        table_name = r['table']
        try:
            r['price'] = int(r['price'])
        except:
            pass
        try:
            r['price_opt'] = int(r['price_opt'])
        except:
            pass
        app_label, model_name = table_name.split('_', 1)  # Разделяем на лейбл приложения и название модели
        model = apps.get_model(app_label=app_label, model_name=model_name)
        line = UniqIdProds.objects.filter(native_id=r['id'], model=f'{(model.__name__).lower()}').first()
        if line:
            r['global_id'] = line.id
        else:
            print('НЕ НАШЛИ ГЛОБАЛ ИД')
            l = UniqIdProds.objects.create(native_id=r['id'], model=f'{(model.__name__).lower()}')
            r['global_id'] = l.id

    all_lines = sorted(all_lines, key=lambda x: x['global_id'], reverse=True)
    return all_lines


def havent_4_now(title, stat):
    rows = get_all_prods()
    unks = get_all_unk_prods()

    for r in rows:
        if r['name'].lower() in title.lower() or title.lower() in r['name'].lower():
            if not stat:
                obj = find_prod_glob(r['global_id'])
                obj.available = 'Нет в наличии'
                obj.save()
                print('Меняем статус')
                return True

    for r in unks:
        if r['name'].lower() in title.lower() or title.lower() in r['name'].lower():
            if not stat:
                obj = UnknownType.objects.get(id=r['id'])
                obj.available = 'Нет в наличии'
                obj.save()
                print('Меняем статус')
                return True

    return False

def find_prod(title=None, chars=None):
    try:
        chars.pop('csrfmiddlewaretoken')
    except:
        pass
    try:
        chars.pop('email')
    except:
        pass
    cat = chars.get('categ', None)
    if cat:
        cat = cat[0]
        chars.pop('categ')
    else:
        cat = None

    chars = {key: value for key, value in chars.items() if value != 'None'}
    chars_ = {**chars}
    yes = chars.get('yes', None)
    no = chars.get('no', None)
    four = chars.get('4order', None)

    if yes: chars.pop('yes')
    elif no: chars.pop('no')
    elif four: chars.pop('4order')

    for k, v in chars_.items():
        chars[k] = v[0]
        if chars[k] == '' or chars[k] == v:
            chars.pop(k)


    if yes:
        chars['available'] = 'В наличии'
        print('Есть ес')
    elif no:
        chars['available'] = 'Нет в наличии'
    elif four:
        chars['available'] = 'Под заказ'

    if chars.get('price', None):
        price = price_validator(str(chars.get('price')))
    else:
        price = None

    chars_ = {**chars}
    prods = []
    if cat:
        obj_mod = find_model(cat.lower())
        if chars:
            char_fields = []
            for field in obj_mod._meta.get_fields():
                if isinstance(field, models.CharField):
                    char_fields.append(field.name)

            if title:
                chars = {**chars, "name__icontains": title}
            if price:
                chars = {**chars, "price__gt": price - ((price / 100) * 30), "price__lt" :(price + ((price / 100) * 30))}
                chars.pop('price')

            for key, value in chars_.items():
                if key == value or not value:
                    continue
                if not hasattr(obj_mod(), key):
                    chars.pop(key)

            updated_chars = {}
            for k, v in chars.items():
                if str(k).lower().find('__icontains') == -1 and k in char_fields:
                    updated_chars[f'{k}__icontains'] = v
                else:
                    updated_chars[k] = v

            chars = updated_chars

            if yes:
                filtered_objs = obj_mod.objects.filter(~Q(available='Нет в наличии'), **chars)
            else:
                filtered_objs = obj_mod.objects.filter(**chars)
            if filtered_objs:
                for obj in filtered_objs:
                    line = UniqIdProds.objects.filter(native_id=obj.id, model=f'{(obj_mod().__class__.__name__).lower()}').first()
                    try:
                        obj.price = int(obj.price)
                    except:
                        pass

                    try:
                        obj.price_opt = int(obj.price_opt)
                    except:
                        pass

                    if line:
                        obj.global_id = line.id

                prods.extend(filtered_objs)
            if title:
                chars = {**chars, "descr__icontains": title}
                chars.pop("name__icontains")
                if yes:
                    filtered_objs = obj_mod.objects.filter(~Q(available='Нет в наличии'), **chars)
                else:
                    filtered_objs = obj_mod.objects.filter(**chars)

                for obj in filtered_objs:
                    try:
                        obj.price = int(obj.price)
                    except:
                        pass

                    try:
                        obj.price_opt = int(obj.price_opt)
                    except:
                        pass
                    line = UniqIdProds.objects.filter(native_id=obj.id,
                                                      model=f'{(obj_mod().__class__.__name__).lower()}').first()
                    if line:
                        obj.global_id = line.id

                prods.extend(filtered_objs)
        else:
            filtered_objs = obj_mod.objects.all()
            for obj in filtered_objs:
                line = UniqIdProds.objects.filter(native_id=obj.id, model=f'{(obj_mod().__class__.__name__).lower()}').first()
                try:
                    obj.price = int(obj.price)
                except:
                    pass

                try:
                    obj.price_opt = int(obj.price_opt)
                except:
                    pass
                if line:
                    obj.global_id = line.id

            prods.extend(filtered_objs)
    else:
        all_models = apps.get_models()
        modelss = []
        for model in all_models:
            if model.__name__ not in ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session',
                                      'User_my', 'History', 'UniqIdProds', 'UnknownType', 'Providers']:
                modelss.append(model)

        for model in modelss:
            chars = {**chars_}
            char_fields = []
            for field in model._meta.get_fields():
                if isinstance(field, models.CharField):
                    char_fields.append(field.name)

            if title:
                chars = {**chars, "name__icontains": title}
            if price:
                chars = {**chars, "price__gt": price - ((price / 100) * 30),
                         "price__lt": (price + ((price / 100) * 30))}
                chars.pop('price')


            if chars:
                for key, value in chars_.items():
                    if key == value or not value:
                        continue
                    if not hasattr(model(), key):
                        chars.pop(key)

                updated_chars = {}
                for k, v in chars.items():
                    if str(k).lower().find('__icontains') == -1 and k in char_fields:
                        updated_chars[f'{k}__icontains'] = v
                    else:
                        updated_chars[k] = v

                chars = updated_chars

            chars = validate_int_fields(chars)
            if yes:
                filtered_objs = model.objects.filter(~Q(available='Нет в наличии'), **chars)
                print('Без нет в наличии фильтр')
            else:
                filtered_objs = model.objects.filter(**chars)

            for obj in filtered_objs:
                try:
                    obj.price = int(obj.price)
                except:
                    pass

                try:
                    obj.price_opt = int(obj.price_opt)
                except:
                    pass
                line = UniqIdProds.objects.filter(native_id=obj.id, model=f'{(model().__class__.__name__).lower()}').first()
                if line:
                    obj.global_id = line.id
            prods.extend(filtered_objs)

            if title:
                chars = {**chars, "descr__icontains": title}
                chars.pop("name__icontains")
                if yes:
                    filtered_objs = model.objects.filter(~Q(available='Нет в наличии'), **chars)
                else:
                    filtered_objs = model.objects.filter(**chars)


                for obj in filtered_objs:
                    try:
                        obj.price = int(obj.price)
                    except:
                        pass

                    try:
                        obj.price_opt = int(obj.price_opt)
                    except:
                        pass
                    line = UniqIdProds.objects.filter(native_id=obj.id,
                                                      model=f'{(model().__class__.__name__).lower()}').first()
                    if line:
                        obj.global_id = line.id
            prods.extend(filtered_objs)

    unique_prods = []
    seen = set()
    for item in prods:
        if type(item) == type({'1': ''}):
            item_tuple = tuple(item.items())
            if item_tuple not in seen:
                unique_prods.append(item)
                seen.add(item_tuple)
        else:
            if item not in seen:
                unique_prods.append(item)
                seen.add(item)

    return unique_prods


def validate_int_fields(chars):
    # Получаем все модели в приложении по умолчанию
    all_models = apps.get_app_config('cat').get_models()

    # Список полей типа IntegerField
    int_fields = [
        field.name
        for model in all_models
        for field in model._meta.get_fields()
        if isinstance(field, models.IntegerField)
    ]

    # Проверяем каждый ключ в словаре chars
    ch = {**chars}
    for key, value in ch.items():
        if key in int_fields and not isinstance(value, int):
            # Удаляем значение ключа, если он соответствует полю типа IntegerField, но не является типом int
            del chars[key]

    return chars

def good_keys_for_chars(dic):
    d = {}
    for k, v in dic.items():
        for cc in c.keys():
            if cc.lower() in k.lower() or k.lower() in cc.lower():
                print(cc, k)
                d = {**d, cc: v}
                continue

    return d

def chat_get_type(title, descr, model="gpt-3.5-turbo-16k"):
    global chat_value
    print('Глабал знач ', chat_value)
    if descr:
        if len(descr) > 300:
            descr = descr[:300]
    else:
        descr = ''

    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer key"
    }
    data = {
        "model": model,
        "messages": [
            {"role": "system", "content": f"""Прочитай описание к товару: {title}, 
        {descr}
        Теперь скажи мне, какая категория из следующих к нему подойдет? И напиши ответ ввиде только этой категории:
        StoveAndOven, Fridges, Dishwashers, ForDrinks, Grills, Toasters, Fryers, Multicookers, KitchenScales, WashingMachines, 
        Dryer, Irons, VacuumCleaners, RobotVacuumCleaner, WaterHeaters, AirConditioners, Fans, Heaters, Sewing, HairStylingDrying, 
        ElectricShavers, PhotoEquipment, Microwave, Lighting, Sockets, Printers, BoardGames, ChildToys, Wires, Routers, Headset,
         Speakers, Microphone, StringedInstruments, KeyboardInstruments, WindInstruments, PercussionInstruments, Accordion, SportsThings, 
         Clothes, MusicAccessories, Another"""},
            {"role": "user", "content": descr}
        ]
    }
    response = requests.post(URLL, headers=headers, json=data)
    # try:
    result = response.json()
    try:
        result = result['choices'][0]['message']['content']
    except:
        time.sleep(27)
        try:
            response = requests.post(URLL, headers=headers, json=data)
            result = response.json()
            print(result)
            result = result['choices'][0]['message']['content']
        except:
            if chat_value < 3:
                try:
                    chat_value += 1
                    return chat_get_type(title, descr, model="gpt-3.5-turbo")
                except:
                    chat_value += 1
                    return chat_get_type(title, descr, model="gpt-3.5-turbo-0613")
            else:
                chat_value = 0
                return ''

    chat_value = 0
    print(result)
    return result

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