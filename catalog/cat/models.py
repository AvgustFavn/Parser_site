from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.auth.models import AbstractUser

from cat.valids import price_validator, true_validator


def truncate_field_value(instance, field):
    max_length = field.max_length
    field_type = field.get_internal_type()

    if field_type == 'CharField' and len(getattr(instance, field.name)) > max_length:
        setattr(instance, field.name, getattr(instance, field.name)[:max_length])


class Electronics(models.Model):
    class Meta:
        abstract = True

    name = models.CharField(max_length=450, unique=True)
    type_of_prod = models.CharField(max_length=30, null=True, default='Н.Д.')  # тип духовки и чайника и тд
    manufacturer_country = models.CharField(max_length=15, null=True, default='Н.Д.')
    company = models.CharField(max_length=30, null=True, default='Н.Д.')
    color = models.CharField(max_length=15, null=True, default='Н.Д.')
    material = models.CharField(max_length=30, null=True, default='Н.Д.')
    display = models.CharField(max_length=30, null=True, default='Н.Д.')
    max_power_consumption = models.CharField(max_length=30, null=True,
                                             default='Н.Д.')  # Максимальная потребляемая мощность
    supply_voltage = models.CharField(max_length=15, null=True, default='Н.Д.')  # Напряжение питания
    equipment = models.CharField(max_length=100, null=True, default='Н.Д.')  # Комплектация
    sizes = models.CharField(max_length=30, null=True, default='Н.Д.')
    weight = models.CharField(max_length=15, null=True, default='Н.Д.')
    programs = models.CharField(max_length=50, null=True, default='Н.Д.')
    energy_class = models.CharField(max_length=7, null=True, default='Н.Д.')
    descr = models.TextField(default='Н.Д.')
    pic = models.CharField(max_length=200, null=True, default='Н.Д.')
    full_desc = models.TextField(null=True, default='Н.Д.')
    price = models.FloatField(null=True, validators=[price_validator]) # Розница
    price_opt = models.FloatField(null=True, validators=[price_validator])
    draft_chars = models.CharField(max_length=300, null=True)
    url = models.URLField(null=True)
    art = models.CharField(max_length=35, null=True, default='Н.Д.')
    available = models.CharField(max_length=35, null=True, default='Н.Д.')

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField):
                max_length = field.max_length
                field_value = getattr(self, field.name)
                if type(field_value) != type(False):
                    if field_value and len(str(field_value)) > max_length:
                        setattr(self, field.name, str(field_value)[:max_length])

            elif isinstance(field, models.IntegerField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2):
                    continue

            elif isinstance(field, models.BooleanField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2.0):
                    continue

        super().save(*args, **kwargs)


class MusicInstruments(models.Model):
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField):
                max_length = field.max_length
                field_value = getattr(self, field.name)
                if type(field_value) != type(False):
                    if field_value and len(str(field_value)) > max_length:
                        setattr(self, field.name, str(field_value)[:max_length])

            elif isinstance(field, models.IntegerField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2):
                    continue

            elif isinstance(field, models.BooleanField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2.0):
                    continue

        super().save(*args, **kwargs)

    name = models.CharField(max_length=200, unique=True)
    type_of_prod = models.CharField(max_length=30, null=True, default='Н.Д.')  # тип духовки и чайника и тд
    manufacturer_country = models.CharField(max_length=15, null=True, default='Н.Д.')
    company = models.CharField(max_length=30, null=True, default='Н.Д.')
    color = models.CharField(max_length=15, null=True, default='Н.Д.')
    material = models.CharField(max_length=30, null=True, default='Н.Д.')
    equipment = models.CharField(max_length=100, null=True, default='Н.Д.')  # Комплектация
    sizes = models.CharField(max_length=30, null=True, default='Н.Д.')
    weight = models.CharField(max_length=15, null=True, default='Н.Д.')
    descr = models.TextField(default='Н.Д.')
    pic = models.CharField(max_length=200, null=True, default='Н.Д.')
    price = models.FloatField(null=True, validators=[price_validator])
    url = models.URLField(null=True, default='Н.Д.')
    art = models.CharField(max_length=35, null=True, default='Н.Д.')
    available = models.CharField(max_length=35, null=True, default='Н.Д.')
    price_opt = models.FloatField(null=True, validators=[price_validator])


class StoveAndOven(Electronics):
    burners = models.CharField(max_length=15, null=True, default='Н.Д.')  # конфорки
    oven_volume = models.CharField(max_length=15, null=True, default='Н.Д.')  # объем печки
    max_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    grill = models.BooleanField(null=True)  # Есть ли гриль
    power_per_burner = models.CharField(max_length=30, null=True, default='Н.Д.')  # Мощность каждой конфорки
    non_stick_coating = models.BooleanField(null=True)  # антипригарка


class Fridges(Electronics):
    volume = models.CharField(max_length=15, null=True, default='Н.Д.')  # объем
    min_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    freezing_power = models.CharField(max_length=15, null=True, default='Н.Д.')
    noise_level = models.CharField(max_length=15, null=True, default='Н.Д.')
    refrigerant = models.CharField(max_length=15, null=True, default='Н.Д.')  # Хладагент
    shelf_material = models.CharField(max_length=15, null=True, default='Н.Д.')
    number_of_shelves = models.CharField(max_length=15, null=True, default='Н.Д.')


class Dishwashers(Electronics):
    volume = models.CharField(max_length=15, null=True, default='Н.Д.')  # объем
    min_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    shelf_material = models.CharField(max_length=15, null=True, default='Н.Д.')
    number_of_shelves = models.CharField(max_length=15, null=True, default='Н.Д.')
    drying_type = models.CharField(max_length=15, null=True, default='Н.Д.')
    max_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    leak_protection_type = models.CharField(max_length=15, null=True, default='Н.Д.')  # Тип защиты от протечек
    salt_indicator = models.CharField(max_length=15, null=True, default='Н.Д.')  # Индикатор соли
    rinse_aid_indicator = models.CharField(max_length=15, null=True, default='Н.Д.')  # Индикатор ополаскивателя
    wash_class = models.CharField(max_length=7, null=True, default='Н.Д.')  # потребление воды
    dry_class = models.CharField(max_length=7, null=True, default='Н.Д.')  # потребление сушки


class ForDrinks(Electronics):
    volume = models.CharField(max_length=15, null=True, default='Н.Д.')  # объем
    min_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    max_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    leak_protection_type = models.CharField(max_length=15, null=True, default='Н.Д.')  # Тип защиты от протечек
    heating_element_type = models.CharField(max_length=15, null=True, default='Н.Д.')  # Тип нагревательного элемента
    filter = models.CharField(max_length=15, null=True, default='Н.Д.')
    temperature_maintenance = models.BooleanField(null=True, validators=[true_validator])  # Поддержание температуры
    water_supply = models.CharField(max_length=15, null=True, default='Н.Д.')  # Подача воды
    type_of_coffee = models.CharField(max_length=30, null=True, default='Н.Д.')
    container_capacity = models.CharField(max_length=30, null=True, default='Н.Д.')
    built_in_coffee_grinder = models.CharField(max_length=30, null=True, default='Н.Д.')


class Grills(Electronics):
    min_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    max_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    heating_element_type = models.CharField(max_length=15, null=True, default='Н.Д.')  # Тип нагревательного элемента
    temperature_maintenance = models.BooleanField(null=True, validators=[true_validator])  # Поддержание температуры
    surface_size = models.CharField(max_length=15, null=True, default='Н.Д.')  # рабочая поверхность
    non_stick_coating = models.BooleanField(null=True)  # антипригарка
    timer = models.BooleanField(null=True)


class Toasters(Electronics):
    number_of_branches = models.IntegerField(null=True)  # Количество отделений
    numbers_of_toasts = models.IntegerField(null=True)  # Количество тостов
    auto_shutdown = models.BooleanField(null=True, validators=[true_validator])  # Автоотключение
    defrosting = models.BooleanField(null=True)  # Разморозка
    browning_levels = models.CharField(max_length=15, null=True, default='Н.Д.')  # Степени обжарки
    stencil = models.BooleanField(null=True, validators=[true_validator])  # Трафарет
    min_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    max_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')


class Fryers(Electronics):
    volume = models.CharField(max_length=15, null=True, default='Н.Д.')  # объем
    non_stick_coating = models.BooleanField(null=True)  # антипригарка
    filter = models.CharField(max_length=15, null=True, default='Н.Д.')
    adjustable_thermostat = models.BooleanField(null=True, validators=[true_validator])  # Регулировка термостата
    auto_oil_drain = models.BooleanField(null=True, validators=[true_validator])  # Автослив масла
    timer = models.BooleanField(null=True)
    min_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    max_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')


class Multicookers(Electronics):
    min_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    max_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    timer = models.BooleanField(null=True)
    volume = models.CharField(max_length=15, null=True, default='Н.Д.')  # объем
    non_stick_coating = models.BooleanField(null=True)  # антипригарка
    temperature_maintenance = models.BooleanField(null=True, validators=[true_validator])  # Поддержание температуры


class KitchenScales(Electronics):
    bowl = models.CharField(max_length=15, null=True, default='Н.Д.')  # Миска
    weighing_limit = models.CharField(max_length=15, null=True, default='Н.Д.')  # До какого веса взвешивать можно
    weighing_accuracy = models.CharField(max_length=7, null=True, default='Н.Д.')  # точность взвешивания
    liquid_volume_measurement = models.BooleanField(null=True)  # Объем жидкости
    battery_type = models.CharField(max_length=7, null=True, default='Н.Д.')
    number_of_batteries = models.IntegerField(null=True, validators=[true_validator])


class WashingMachines(Electronics):
    download_type = models.CharField(max_length=15, null=True, default='Н.Д.')  # Загрузка вещей спереди или нет
    maximum_weight = models.CharField(max_length=15, null=True, default='Н.Д.')
    maximum_weight_to_dry = models.CharField(max_length=15, null=True, default='Н.Д.')
    min_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    max_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    noise_level = models.CharField(max_length=15, null=True, default='Н.Д.')
    water_consumption = models.CharField(max_length=15, null=True, default='Н.Д.')  # Потребление воды
    max_spin_speed = models.CharField(max_length=15, null=True, default='Н.Д.')


class Dryer(Electronics):
    drying_type = models.CharField(max_length=15, null=True, default='Н.Д.')
    volume = models.CharField(max_length=15, null=True, default='Н.Д.')  # объем
    maximum_weight_to_dry = models.CharField(max_length=15, null=True, default='Н.Д.')
    noise_level = models.CharField(max_length=15, null=True, default='Н.Д.')


class Irons(Electronics):
    min_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    max_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    sole_material = models.CharField(max_length=15, null=True, default='Н.Д.')  # Материал подошвы
    water_tank_volume = models.CharField(max_length=15, null=True, default='Н.Д.')  # Резюрвар для воды
    supply_steam = models.CharField(max_length=15, null=True, default='Н.Д.')
    wireless = models.BooleanField(null=True)
    self_cleaning = models.CharField(max_length=15, null=True, default='Н.Д.')


class VacuumCleaners(Electronics):
    type_cleaning = models.CharField(max_length=15, null=True, default='Н.Д.')  # Тип уборки
    dust_capacity = models.CharField(max_length=15, null=True, default='Н.Д.')  # Емкость пылесборника
    pipe = models.CharField(max_length=15, null=True, default='Н.Д.')  # Труба
    noise_level = models.CharField(max_length=15, null=True)
    power_regulator = models.CharField(25, null=True)


class RobotVacuumCleaner(Electronics):
    type_cleaning = models.CharField(max_length=15, null=True, default='Н.Д.')  # Тип уборки
    dust_capacity = models.CharField(max_length=15, null=True, default='Н.Д.')  # Емкость пылесборника
    noise_level = models.CharField(max_length=15, null=True, default='Н.Д.')
    sensor_types = models.CharField(max_length=15, null=True, default='Н.Д.')
    control = models.CharField(max_length=15, null=True, default='Н.Д.')
    management_app = models.CharField(max_length=15, null=True, default='Н.Д.')
    station = models.BooleanField(null=True)
    scheduled_cleaning = models.BooleanField()  # Уборка по расписанию
    battery_life = models.CharField(max_length=15, null=True, default='Н.Д.')
    charging_time = models.CharField(max_length=15, null=True, default='Н.Д.')


class WaterHeaters(Electronics):
    volume = models.CharField(max_length=15, null=True, default='Н.Д.')  # объем
    min_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    max_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')
    mounting_method = models.CharField(max_length=15, null=True, default='Н.Д.')  # Способ крепления
    max_water_pressure = models.CharField(max_length=15, null=True, default='Н.Д.')
    temperature_display = models.BooleanField(null=True)
    shower_head = models.BooleanField(null=True)
    maximum_performance = models.CharField(max_length=15, null=True, default='Н.Д.')  # Макс производительность
    gas_inlet_outlet = models.CharField(max_length=25, null=True, default='Н.Д.')  # вход газа
    gas_control = models.BooleanField(null=True)
    recycling = models.BooleanField(null=True)
    fuel_type = models.CharField(max_length=15, null=True, default='Н.Д.')
    gas_consumption = models.CharField(max_length=15, null=True, default='Н.Д.')  # расход газа


class AirConditioners(Electronics):
    cooling_capacity = models.CharField(max_length=15, null=True, default='Н.Д.')  # Холодопроизводительность
    cooling_power = models.CharField(max_length=15, null=True, default='Н.Д.')  # Мощность охлаждения
    heating_power = models.CharField(max_length=15, null=True, default='Н.Д.')  # Мощность обогрева
    recommended_room_area = models.CharField(max_length=15, null=True, default='Н.Д.')
    dehumidification_intensity = models.CharField(max_length=15, null=True, default='Н.Д.')  # Интенсивность осушения
    noise_level = models.CharField(max_length=15, null=True, default='Н.Д.')
    refrigerant = models.CharField(max_length=15, null=True, default='Н.Д.')  # Хладагент
    filter = models.CharField(max_length=15, null=True, default='Н.Д.')
    air_flow = models.CharField(max_length=15, null=True, default='Н.Д.')  # Воздушный поток


class Fans(Electronics):
    scope_of_application = models.CharField(max_length=15, null=True, default='Н.Д.')  # Сфера применения
    mounting_method = models.CharField(max_length=15, null=True, default='Н.Д.')  # Способ крепления
    power_regulator = models.CharField(25, null=True)
    adjustable_thermostat = models.BooleanField(null=True, validators=[true_validator])  # Регулировка термостата
    recommended_room_area = models.CharField(max_length=15, null=True, default='Н.Д.')


class Heaters(Electronics):  # Обогреватель
    mounting_method = models.CharField(max_length=15, null=True, default='Н.Д.')  # Способ крепления
    fuel = models.CharField(max_length=15, null=True, default='Н.Д.')
    fuel_consumption = models.CharField(max_length=15, null=True, default='Н.Д.')  # Расход топлива
    power_regulator = models.CharField(25, null=True)
    recommended_room_area = models.CharField(max_length=15, null=True, default='Н.Д.')
    fan = models.BooleanField(null=True)
    handle_wheels = models.CharField(max_length=15, null=True, default='Н.Д.')
    adjustable_thermostat = models.BooleanField(null=True, validators=[true_validator])  # Регулировка термостата
    air_flow = models.CharField(max_length=15, null=True, default='Н.Д.')  # Воздушный поток


class Sewing(Electronics):  # Швейные машинки
    machine_type = models.CharField(max_length=15, null=True, default='Н.Д.')  # Тип машинки
    shuttle_type = models.CharField(max_length=15, null=True, default='Н.Д.')  # Тип челнока
    pedal = models.BooleanField(null=True)
    sewing_speed_adjustment = models.CharField(max_length=25, null=True, default='Н.Д.')  # Регулировка скорости шитья
    double_needle = models.CharField(max_length=25, null=True, default='Н.Д.')  # Двойная игла
    backlight = models.CharField(max_length=25, null=True, default='Н.Д.')  # Подсветка
    сompartment_for_accessories = models.CharField(max_length=25, null=True, default='Н.Д.')  # Отсек для аксессуаров
    max_number_threads = models.CharField(max_length=25, null=True, default='Н.Д.')  # Максимальное число нитей
    max_sewing_speed = models.CharField(max_length=15, null=True, default='Н.Д.')  # Максимальная скорость шитья
    trays = models.CharField(max_length=15, null=True, default='Н.Д.')  # Лотки


class HairStylingDrying(Electronics):  # Уход за волосами
    filter = models.BooleanField(null=True)
    overheat_protection = models.CharField(max_length=15, null=True, default='Н.Д.')  # защита от перегрева
    nozzles = models.CharField(max_length=15, null=True, default='Н.Д.')  # Насадки
    speeds = models.CharField(max_length=30, null=True, default='Н.Д.')
    cold_air = models.BooleanField(null=True)
    heating_time = models.CharField(max_length=15, null=True, default='Н.Д.')  # Время для нагрева
    temp_step_adjustment = models.CharField(max_length=15, null=True, default='Н.Д.')  # Степени температуры
    max_temperature = models.CharField(max_length=15, null=True, default='Н.Д.')


class ElectricShavers(Electronics):
    nozzles = models.CharField(max_length=15, null=True, default='Н.Д.')  # Насадки
    self_sharpening_knives = models.BooleanField(null=True, validators=[true_validator])
    blade_lubrication = models.CharField(max_length=15, null=True, default='Н.Д.')  # Смазка лезвий
    power = models.CharField(max_length=15, null=True, default='Н.Д.')  # Питание
    blade_material = models.CharField(max_length=15, null=True, default='Н.Д.')
    power_regulator = models.CharField(25, null=True)
    сharging_time = models.CharField(max_length=15, null=True, default='Н.Д.')
    shaving_method = models.CharField(max_length=15, null=True, default='Н.Д.')


class PhotoEquipment(Electronics):
    total_number_megapix_matrix = models.CharField(max_length=15, null=True,
                                                   default='Н.Д.')  # Общее число мегапикселей матрицы
    effective_megapixels = models.CharField(max_length=15, null=True, default='Н.Д.')  # Число эффективных мегапикселей
    matrix_type = models.CharField(max_length=15, null=True, default='Н.Д.')
    phys_size_matrix = models.CharField(max_length=15, null=True, default='Н.Д.')
    crop_factor = models.CharField(max_length=7, null=True, default='Н.Д.')
    full_frame = models.BooleanField(null=True, validators=[true_validator])  # Полнокадровый
    maximum_resolution = models.CharField(max_length=15, null=True, default='Н.Д.')
    iso = models.CharField(max_length=30, null=True, default='Н.Д.')
    flash = models.BooleanField(null=True)
    lens = models.CharField(max_length=30, null=True, default='Н.Д.')
    focal_length = models.CharField(max_length=20, null=True, default='Н.Д.')
    aperture_value = models.CharField(max_length=30, null=True, default='Н.Д.')
    excerpt = models.CharField(max_length=30, null=True, default='Н.Д.')
    image_formats = models.CharField(max_length=20, null=True, default='Н.Д.')
    q4k_support = models.CharField(max_length=20, null=True, default='Н.Д.')
    q1080_support = models.CharField(max_length=20, null=True, default='Н.Д.')
    image_sensor_cleaning_function = models.BooleanField(null=True)
    cpu = models.CharField(max_length=20, null=True, default='Н.Д.')
    diaphragm = models.CharField(max_length=20, null=True, default='Н.Д.')
    flash_range = models.CharField(max_length=7, null=True, default='Н.Д.')
    supported_memory_cards = models.CharField(max_length=20, null=True, default='Н.Д.')
    viewing_angle = models.CharField(max_length=7, null=True, default='Н.Д.')  # Угол обзора
    image_stabilization = models.BooleanField(null=True, validators=[true_validator])
    timelapse = models.BooleanField(null=True, validators=[true_validator])
    maximum_memory_card_size = models.CharField(max_length=7, null=True, default='Н.Д.')
    recording_video_format = models.CharField(max_length=7, null=True, default='Н.Д.')


class Microwave(Electronics):
    volume = models.CharField(max_length=7, null=True, default='Н.Д.')
    backlight = models.BooleanField(null=True)  # Подсветка
    pallet_diameter = models.CharField(max_length=20, null=True, default='Н.Д.')
    power_regulator = models.CharField(25, null=True)
    max_timer = models.CharField(max_length=20, null=True, default='Н.Д.')
    delay_start = models.BooleanField(null=True)
    pause = models.BooleanField(null=True)
    grill = models.BooleanField(null=True)


class Lighting(Electronics):
    plinth = models.CharField(max_length=7, null=True, default='Н.Д.')  # Цокль
    flask_color = models.CharField(max_length=7, null=True, default='Н.Д.')
    spectrum_quality = models.CharField(max_length=10, null=True, default='Н.Д.')  # Цвет света
    num_working_hours = models.CharField(max_length=7, null=True, default='Н.Д.')
    light_source_type = models.CharField(max_length=10, null=True, default='Н.Д.')  # Тип источника света
    num_light_sources = models.CharField(max_length=30, null=True, default='Н.Д.')  # количество ист. света
    mounting_method = models.CharField(max_length=7, null=True, default='Н.Д.')  # Крепление
    max_lighting_area = models.CharField(max_length=7, null=True, default='Н.Д.')
    lamp_shape = models.CharField(max_length=10, null=True, default='Н.Д.')
    degree_protection = models.CharField(max_length=10, null=True, default='Н.Д.')
    ripples = models.CharField(max_length=10, null=True, default='Н.Д.')  # Пульсация
    shade_direction = models.CharField(max_length=10, null=True, default='Н.Д.')  # Направление плафона
    operating_temperatures = models.CharField(max_length=20)  # Раб. температуры
    num_leds = models.CharField(max_length=20)


class Sockets(Electronics):  # Розетка
    internal_dimensions = models.CharField(max_length=30, null=True, default='Н.Д.')  # Внутренние габариты
    degree_protection = models.CharField(max_length=30, null=True, default='Н.Д.')
    num_keys = models.CharField(max_length=25, null=True, default='Н.Д.')
    rated_current = models.CharField(max_length=25, null=True, default='Н.Д.')  # Номинальный ток
    lid = models.BooleanField(null=True, validators=[true_validator])
    nests = models.CharField(max_length=40, null=True, default='Н.Д.')  # Гнезды
    bandwidth = models.CharField(max_length=35, null=True, default='Н.Д.')  # Полоса частот
    grounding = models.BooleanField(null=True)


class Printers(Electronics):
    print_resolution = models.CharField(max_length=20, null=True, default='Н.Д.')  # Разрешение печати
    print_speed = models.CharField(max_length=10, null=True, default='Н.Д.')
    connectivity = models.CharField(max_length=10, null=True, default='Н.Д.')  # технология подключения
    duplex_printing = models.BooleanField(null=True, validators=[true_validator])
    supported_paper_sizes = models.CharField(max_length=20, null=True, default='Н.Д.')  # Поддерживаемые форматы бумаг
    noise_level = models.CharField(max_length=15, null=True, default='Н.Д.')
    print_technology = models.CharField(max_length=15, null=True, default='Н.Д.')  # Допустим лазерная
    print_color = models.CharField(max_length=15, null=True, default='Н.Д.')
    supported_media_weights = models.CharField(max_length=20, null=True,
                                               default='Н.Д.')  # Поддерживаемая плотность носителей
    scanner = models.BooleanField(null=True, validators=[true_validator])


class BoardGames(models.Model):
    name = models.CharField(max_length=200, null=True, default='Н.Д.', unique=True)
    pic = models.CharField(max_length=200, null=True, default='Н.Д.')
    company = models.CharField(max_length=30, null=True, default='Н.Д.')
    publishing_house = models.CharField(max_length=30, null=True, default='Н.Д.')
    num_players = models.CharField(max_length=10, null=True, default='Н.Д.')
    game_time = models.CharField(max_length=10, null=True, default='Н.Д.')
    age_restrictions = models.FloatField(null=True, validators=[price_validator])
    genre = models.CharField(max_length=10, null=True, default='Н.Д.')
    descr = models.TextField(default='Н.Д.')
    equipment = models.CharField(max_length=100, null=True, default='Н.Д.')
    lang = models.CharField(max_length=10, null=True, default='Н.Д.')
    full_desc = models.TextField(null=True, default='Н.Д.')
    price = models.FloatField(null=True, validators=[price_validator])
    url = models.URLField(null=True, default='Н.Д.')
    art = models.CharField(max_length=35, null=True, default='Н.Д.')
    available = models.CharField(max_length=35, null=True, default='Н.Д.')
    price_opt = models.FloatField(null=True, validators=[price_validator])

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField):
                max_length = field.max_length
                field_value = getattr(self, field.name)
                if type(field_value) != type(False):
                    if field_value and len(str(field_value)) > max_length:
                        setattr(self, field.name, str(field_value)[:max_length])

            elif isinstance(field, models.IntegerField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2):
                    continue

            elif isinstance(field, models.BooleanField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2.0):
                    continue

        super().save(*args, **kwargs)


class ChildToys(models.Model):
    name = models.CharField(max_length=200, null=True, default='Н.Д.', unique=True)
    type_of_prod = models.CharField(max_length=30, null=True, default='Н.Д.')  # тип духовки и чайника и тд
    manufacturer_country = models.CharField(max_length=15, null=True, default='Н.Д.')
    age_restrictions = models.FloatField(null=True, validators=[price_validator])
    company = models.CharField(max_length=30, null=True, default='Н.Д.')
    color = models.CharField(max_length=15, null=True, default='Н.Д.')
    material = models.CharField(max_length=30, null=True, default='Н.Д.')
    sizes = models.CharField(max_length=30, null=True, default='Н.Д.')
    weight = models.CharField(max_length=15, null=True, default='Н.Д.')
    descr = models.TextField(default='Н.Д.')
    pic = models.CharField(max_length=200, null=True, default='Н.Д.')
    safety = models.CharField(max_length=30, null=True, default='Н.Д.')
    full_desc = models.TextField(null=True, default='Н.Д.')
    price = models.FloatField(null=True, validators=[price_validator])
    sense = models.CharField(max_length=50, null=True, default='Н.Д.')
    url = models.URLField(null=True, default='Н.Д.')
    art = models.CharField(max_length=35, null=True, default='Н.Д.')
    available = models.CharField(max_length=35, null=True, default='Н.Д.')
    price_opt = models.FloatField(null=True, validators=[price_validator])

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField):
                max_length = field.max_length
                field_value = getattr(self, field.name)
                if type(field_value) != type(False):
                    if field_value and len(str(field_value)) > max_length:
                        setattr(self, field.name, str(field_value)[:max_length])

            elif isinstance(field, models.IntegerField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2):
                    continue

            elif isinstance(field, models.BooleanField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2.0):
                    continue

        super().save(*args, **kwargs)


class Wires(models.Model):
    name = models.CharField(max_length=200, null=True, default='Н.Д.', unique=True)
    manufacturer_country = models.CharField(max_length=15, null=True, default='Н.Д.')
    company = models.CharField(max_length=60, null=True, default='Н.Д.')
    color = models.CharField(max_length=15, null=True, default='Н.Д.')
    material = models.CharField(max_length=60, null=True, default='Н.Д.')
    sizes = models.CharField(max_length=30, null=True, default='Н.Д.')
    descr = models.TextField(default='Н.Д.')
    pic = models.CharField(max_length=200, null=True, default='Н.Д.')
    conductor = models.CharField(max_length=30, null=True, default='Н.Д.')  # Проводник
    insulation = models.CharField(max_length=30, null=True, default='Н.Д.')  # Изоляция
    screen = models.CharField(max_length=40, null=True, default='Н.Д.')
    electrical_resistance = models.CharField(max_length=60, null=True, default='Н.Д.')  # Электрическое сопротивление
    electrical_capacitance = models.CharField(max_length=60, null=True, default='Н.Д.')  # Электрическая емкость
    propagation_speed = models.CharField(max_length=30, null=True, default='Н.Д.')  # Скорость распространения
    temp = models.CharField(max_length=30, null=True, default='Н.Д.')  # Рабочая температура
    working_voltage = models.CharField(max_length=40, null=True, default='Н.Д.')
    weight = models.CharField(max_length=15, null=True, default='Н.Д.')
    full_desc = models.TextField(null=True, default='Н.Д.')
    price = models.FloatField(null=True, validators=[price_validator])
    url = models.URLField(null=True, default='Н.Д.')
    art = models.CharField(max_length=35, null=True, default='Н.Д.')
    available = models.CharField(max_length=35, null=True, default='Н.Д.')
    price_opt = models.FloatField(null=True, validators=[price_validator])

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField):
                max_length = field.max_length
                field_value = getattr(self, field.name)
                if type(field_value) != type(False):
                    if field_value and len(str(field_value)) > max_length:
                        setattr(self, field.name, str(field_value)[:max_length])

            elif isinstance(field, models.IntegerField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2):
                    continue

            elif isinstance(field, models.BooleanField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2.0):
                    continue

        super().save(*args, **kwargs)


class Routers(Electronics):
    standard = models.CharField(max_length=10, null=True, default='Н.Д.')  # стандарт wifi
    max_speed = models.CharField(max_length=10, null=True, default='Н.Д.')
    ranges = models.CharField(max_length=30, null=True, default='Н.Д.')  # сколько диапазонов частот
    transmitter_power = models.CharField(max_length=10, null=True, default='Н.Д.')  # Мощность передатчика
    security = models.CharField(max_length=30, null=True, default='Н.Д.')
    ports = models.CharField(max_length=30, null=True, default='Н.Д.')
    usb = models.BooleanField(null=True)


class UnknownType(models.Model):
    name = models.CharField(max_length=200, null=True, default='Н.Д.', unique=True)
    datas = models.JSONField()
    available = models.CharField(max_length=35, null=True, default='Н.Д.')

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField):
                max_length = field.max_length
                field_value = getattr(self, field.name)
                if type(field_value) != type(False):
                    if field_value and len(str(field_value)) > max_length:
                        setattr(self, field.name, str(field_value)[:max_length])

            elif isinstance(field, models.IntegerField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2):
                    continue

            elif isinstance(field, models.BooleanField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2.0):
                    continue

        super().save(*args, **kwargs)


class Headset(Electronics):
    minimum_repeatable_frequency = models.CharField(max_length=25, null=True, default='Н.Д.')
    resistance = models.CharField(max_length=25, null=True, default='Н.Д.')
    sensitivity = models.CharField(max_length=25, null=True, default='Н.Д.')
    mike = models.BooleanField(default=False, null=True)
    bluetooth = models.BooleanField(default=False, null=True)
    radius = models.CharField(max_length=25, null=True, default='Н.Д.')
    battery_life = models.CharField(max_length=15, null=True, default='Н.Д.')
    charging_time = models.CharField(max_length=15, null=True, default='Н.Д.')
    connection_type = models.CharField(max_length=25, null=True, default='Н.Д.')
    nests = models.CharField(max_length=25, null=True, default='Н.Д.')


class Speakers(Electronics):
    power = models.CharField(max_length=25, null=True, default='Н.Д.')
    minimum_repeatable_frequency = models.CharField(max_length=25, null=True, default='Н.Д.')
    bluetooth = models.BooleanField(default=False, null=True)
    radius = models.CharField(max_length=25, null=True, default='Н.Д.')
    battery_life = models.CharField(max_length=15, null=True, default='Н.Д.')
    charging_time = models.CharField(max_length=15, null=True, default='Н.Д.')
    memory_cards_slot = models.BooleanField(default=False, null=True)
    connection_type = models.CharField(max_length=25, null=True, default='Н.Д.')
    nests = models.CharField(max_length=25, null=True, default='Н.Д.')


class Microphone(Electronics):
    operating_principle = models.CharField(max_length=25, null=True, default='Н.Д.')
    sensitivity = models.CharField(max_length=25, null=True, default='Н.Д.')
    resistance = models.CharField(max_length=25, null=True, default='Н.Д.')
    bluetooth = models.BooleanField(default=False, null=True)
    radius = models.CharField(max_length=25, null=True, default='Н.Д.')
    connection_type = models.CharField(max_length=25, null=True, default='Н.Д.')
    nests = models.CharField(max_length=25, null=True, default='Н.Д.')


class StringedInstruments(MusicInstruments):
    pegs = models.CharField(max_length=25, null=True, default='Н.Д.')  # колки
    mensura = models.CharField(max_length=25, null=True, default='Н.Д.')
    pickup = models.CharField(max_length=25, null=True, default='Н.Д.')  # звукосниматель
    quarters = models.CharField(max_length=25, null=True, default='Н.Д.')  # сколько четвертей
    chinrest = models.CharField(max_length=25, null=True, default='Н.Д.')  # подбородник
    bow = models.CharField(max_length=25, null=True, default='Н.Д.')


class KeyboardInstruments(MusicInstruments):
    num_keys = models.CharField(max_length=25, null=True, default='Н.Д.')
    octaves = models.CharField(max_length=25, null=True, default='Н.Д.')
    key_sensitivity = models.CharField(max_length=25, null=True, default='Н.Д.')
    power = models.CharField(max_length=25, null=True, default='Н.Д.')
    nests = models.CharField(max_length=25, null=True, default='Н.Д.')
    pedals = models.CharField(max_length=25, null=True, default='Н.Д.')
    timbres = models.CharField(max_length=25, null=True, default='Н.Д.')
    bluetooth = models.BooleanField(default=False, null=True)


class WindInstruments(MusicInstruments):
    regime = models.CharField(max_length=25, null=True, default='Н.Д.')  # Строй
    parts = models.CharField(max_length=25, null=True, default='Н.Д.')
    valves = models.CharField(max_length=25, null=True, default='Н.Д.')  # Клапаны, вентели
    quarters = models.CharField(max_length=25, null=True, default='Н.Д.')  # сколько четвертей


class PercussionInstruments(MusicInstruments):  # ударные
    pads = models.CharField(max_length=25, null=True, default='Н.Д.')  # пэды и тарелки
    nests = models.CharField(max_length=25, null=True, default='Н.Д.')


class Accordion(MusicInstruments):
    right = models.CharField(max_length=25, null=True, default='Н.Д.')
    left = models.CharField(max_length=25, null=True, default='Н.Д.')
    register = models.CharField(max_length=25, null=True, default='Н.Д.')
    quarters = models.CharField(max_length=25, null=True, default='Н.Д.')  # сколько четвертей
    ranks = models.CharField(max_length=25, null=True, default='Н.Д.')  # ряды


class SportsThings(models.Model):
    name = models.CharField(max_length=200, null=True, default='Н.Д.', unique=True)
    manufacturer_country = models.CharField(max_length=15, null=True, default='Н.Д.')
    company = models.CharField(max_length=60, null=True, default='Н.Д.')
    color = models.CharField(max_length=15, null=True, default='Н.Д.')
    material = models.CharField(max_length=60, null=True, default='Н.Д.')
    sizes = models.CharField(max_length=30, null=True, default='Н.Д.')
    descr = models.TextField(default='Н.Д.')
    pic = models.CharField(max_length=200, null=True, default='Н.Д.')
    weight = models.CharField(max_length=15, null=True, default='Н.Д.')
    price = models.FloatField(null=True, validators=[price_validator])
    url = models.URLField(null=True, default='Н.Д.')
    art = models.CharField(max_length=35, null=True, default='Н.Д.')
    type_of_prod = models.CharField(max_length=30, null=True, default='Н.Д.')
    available = models.CharField(max_length=35, null=True, default='Н.Д.')
    price_opt = models.FloatField(null=True, validators=[price_validator])

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField):
                max_length = field.max_length
                field_value = getattr(self, field.name)
                if type(field_value) != type(False):
                    if field_value and len(str(field_value)) > max_length:
                        setattr(self, field.name, str(field_value)[:max_length])

            elif isinstance(field, models.IntegerField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2):
                    continue

            elif isinstance(field, models.BooleanField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2.0):
                    continue

        super().save(*args, **kwargs)


class Clothes(models.Model):
    name = models.CharField(max_length=200, null=True, default='Н.Д.', unique=True)
    manufacturer_country = models.CharField(max_length=15, null=True, default='Н.Д.')
    company = models.CharField(max_length=60, null=True, default='Н.Д.')
    color = models.CharField(max_length=15, null=True, default='Н.Д.')
    material = models.CharField(max_length=60, null=True, default='Н.Д.')
    sizes = models.CharField(max_length=30, null=True, default='Н.Д.')
    descr = models.TextField(default='Н.Д.')
    pic = models.CharField(max_length=200, null=True, default='Н.Д.')
    weight = models.CharField(max_length=15, null=True, default='Н.Д.')
    price = models.FloatField(null=True, validators=[price_validator])
    url = models.URLField(null=True, default='Н.Д.')
    art = models.CharField(max_length=35, null=True, default='Н.Д.')
    type_of_prod = models.CharField(max_length=30, null=True, default='Н.Д.')
    available = models.CharField(max_length=35, null=True, default='Н.Д.')
    price_opt = models.FloatField(null=True, validators=[price_validator])

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField):
                max_length = field.max_length
                field_value = getattr(self, field.name)
                if type(field_value) != type(False):
                    if field_value and len(str(field_value)) > max_length:
                        setattr(self, field.name, str(field_value)[:max_length])

            elif isinstance(field, models.IntegerField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2):
                    continue

            elif isinstance(field, models.BooleanField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2.0):
                    continue

        super().save(*args, **kwargs)


class MusicAccessories(models.Model):
    name = models.CharField(max_length=200, null=True, default='Н.Д.', unique=True)
    manufacturer_country = models.CharField(max_length=15, null=True, default='Н.Д.')
    company = models.CharField(max_length=60, null=True, default='Н.Д.')
    color = models.CharField(max_length=15, null=True, default='Н.Д.')
    material = models.CharField(max_length=60, null=True, default='Н.Д.')
    sizes = models.CharField(max_length=30, null=True, default='Н.Д.')
    descr = models.TextField(default='Н.Д.')
    pic = models.CharField(max_length=200, null=True, default='Н.Д.')
    weight = models.CharField(max_length=15, null=True, default='Н.Д.')
    price = models.FloatField(null=True, validators=[price_validator])
    url = models.URLField(null=True, default='Н.Д.')
    art = models.CharField(max_length=35, null=True, default='Н.Д.')
    type_of_prod = models.CharField(max_length=30, null=True, default='Н.Д.')
    available = models.CharField(max_length=35, null=True, default='Н.Д.')
    price_opt = models.FloatField(null=True, validators=[price_validator])

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField):
                max_length = field.max_length
                field_value = getattr(self, field.name)
                if type(field_value) != type(False):
                    if field_value and len(str(field_value)) > max_length:
                        setattr(self, field.name, str(field_value)[:max_length])

            elif isinstance(field, models.IntegerField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2):
                    continue

            elif isinstance(field, models.BooleanField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2.0):
                    continue

        super().save(*args, **kwargs)


class Another(models.Model):
    name = models.CharField(max_length=200, null=True, default='Н.Д.', unique=True)
    manufacturer_country = models.CharField(max_length=15, null=True, default='Н.Д.')
    company = models.CharField(max_length=60, null=True, default='Н.Д.')
    color = models.CharField(max_length=15, null=True, default='Н.Д.')
    material = models.CharField(max_length=60, null=True, default='Н.Д.')
    sizes = models.CharField(max_length=30, null=True, default='Н.Д.')
    descr = models.TextField(default='Н.Д.')
    pic = models.CharField(max_length=200, null=True, default='Н.Д.')
    weight = models.CharField(max_length=15, null=True, default='Н.Д.')
    price = models.FloatField(null=True, validators=[price_validator])
    url = models.URLField(null=True, default='Н.Д.')
    art = models.CharField(max_length=35, null=True, default='Н.Д.')
    type_of_prod = models.CharField(max_length=30, null=True, default='Н.Д.')
    available = models.CharField(max_length=35, null=True, default='Н.Д.')
    price_opt = models.FloatField(null=True, validators=[price_validator])

    def save(self, *args, **kwargs):
        for field in self._meta.get_fields():
            if isinstance(field, models.CharField):
                max_length = field.max_length
                field_value = getattr(self, field.name)
                if type(field_value) != type(False):
                    if field_value and len(str(field_value)) > max_length:
                        setattr(self, field.name, str(field_value)[:max_length])
            elif isinstance(field, models.IntegerField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2):
                    continue

            elif isinstance(field, models.BooleanField):
                field_value = getattr(self, field.name)
                if type(field_value) != type(2.0):
                    continue

        super().save(*args, **kwargs)


class CustomUserManager(BaseUserManager):
    def create_user(self, name, email, password, **extra_fields):
        if not email:
            raise ValueError('Email address is required')

        user = self.model(name=name, email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(name, email, password, **extra_fields)


class User_my(AbstractBaseUser):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=30, unique=True)
    pass_hash = models.CharField(max_length=200)
    status = models.CharField(max_length=15, null=True, default='Клиент')
    img = models.CharField(max_length=200, null=True, default='Н.Д.')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = CustomUserManager()


class History(models.Model):
    i_c = models.CharField(max_length=30)
    done = models.TextField(default='Н.Д.')
    date_of_change = models.DateField()
    title_prod = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        try:
            for field in self._meta.get_fields():
                if isinstance(field, models.CharField):
                    max_length = field.max_length
                    field_value = getattr(self, field.name)
                    if type(field_value) != type(False):
                        if field_value and len(str(field_value)) > max_length:
                            setattr(self, field.name, str(field_value)[:max_length])

                elif isinstance(field, models.BooleanField):
                    field_value = getattr(self, field.name)
                    if type(field_value) != type(2.0):
                        continue

                elif isinstance(field, models.IntegerField):
                    field_value = getattr(self, field.name)
                    if type(field_value) != type(2):
                        continue

            super().save(*args, **kwargs)
        except:
            for field in self._meta.get_fields():
                truncate_field_value(self, field)

            super().save(*args, **kwargs)


class UniqIdProds(models.Model):
    native_id = models.IntegerField()
    model = models.CharField(max_length=65, default=None)

    class Meta:
        app_label = 'cat'

class Providers(models.Model):
    name = models.CharField(max_length=200, unique=True)
    col_name_prod = models.CharField(max_length=10)
    col_art = models.CharField(max_length=10, default='Н.Д.')
    col_retail_price = models.CharField(max_length=10, default='Н.Д.')  # розница
    col_wholesale_price = models.CharField(max_length=10, default='Н.Д.')  # оптовая
    col_descr = models.CharField(max_length=10, default='Н.Д.')
    col_edge = models.CharField(max_length=10, default='Н.Д.')
    col_edge_mosc = models.CharField(max_length=10, default='Н.Д.')
    col_edge_irk = models.CharField(max_length=10, default='Н.Д.')
    col_edge_novos = models.CharField(max_length=10, default='Н.Д.')
    col_pic = models.CharField(max_length=10, default='Н.Д.')
    col_sale = models.CharField(max_length=10, default='Н.Д.')
    col_free = models.CharField(max_length=10, default='Н.Д.')

    def save(self, *args, **kwargs):
        try:
            for field in self._meta.get_fields():
                if isinstance(field, models.CharField):
                    max_length = field.max_length
                    field_value = getattr(self, field.name)
                    if type(field_value) != type(False):
                        if field_value and len(str(field_value)) > max_length:
                            setattr(self, field.name, str(field_value)[:max_length])

                elif isinstance(field, models.BooleanField):
                    field_value = getattr(self, field.name)
                    if type(field_value) != type(2.0):
                        continue
                elif isinstance(field, models.IntegerField):
                    field_value = getattr(self, field.name)
                    if type(field_value) != type(2):
                        continue

            super().save(*args, **kwargs)
        except:
            for field in self._meta.get_fields():
                truncate_field_value(self, field)

            super().save(*args, **kwargs)

