from django.apps import apps
from django.contrib.contenttypes.models import ContentType
from django.db import connection

from cat.models import *


def add_ids():
    models = [
        StoveAndOven, Fridges, Dishwashers, ForDrinks, Grills, Toasters, Fryers, Multicookers,
        KitchenScales, WashingMachines, Dryer, Irons, VacuumCleaners, RobotVacuumCleaner,
        WaterHeaters, AirConditioners, Fans, Heaters, Sewing, HairStylingDrying, ElectricShavers,
        PhotoEquipment, Microwave, Lighting, Sockets, Printers, BoardGames, ChildToys, Wires,
        Routers, Headset, Speakers, Microphone, StringedInstruments, KeyboardInstruments,
        WindInstruments, PercussionInstruments, Accordion, SportsThings, Clothes, MusicAccessories
    ]

    for model in models:
        queris = model.objects.all()
        for q in queris:
            UniqIdProds.objects.create(
            native_id=int(q.id),
            model=f'{str(q.__class__.__name__).lower()}'
            )


def get_all_datas():
    tables = connection.introspection.table_names()
    selected_tables = [table for table in tables if
                       table.startswith('cat_') and not table.endswith('my') and not table.startswith(
                           'cat_unk') and not table.startswith('cat_hist') and not table.startswith('cat_uniq')]
    all_records = []

    for table in selected_tables:
        model_name = table.replace('cat_', '')  # Извлекаем имя модели из названия таблицы
        Model = apps.get_model(app_label='cat', model_name=model_name)  # Замените 'cat' на фактическую метку вашего приложения

        records = Model.objects.all().values('id')
        if records:
            for record in records:
                record['model'] = model_name  # Добавляем поле 'model' с именем модели
                all_records.append(record)

    return all_records
