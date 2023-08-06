import re

from cat.parsing_back import common_words


def find_characteristics(text):
    characteristics = {}
    for key, words in common_words.items():
        for word in words:
            if word.lower() in text.lower():
                if key == 'размеры':
                    regex = r"(?i)(?:размер|вес|масса)[\s:-]+(?:\S+\s+){0,2}?(\w{1,}\s\w{1,}).*?"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[word] = match.group(1)

                elif key == 'материал':
                    s = text[text.lower().find(word):]
                    f = s[:s.lower().find('.')]
                    characteristics[key] = f

                elif key == 'Производитель':
                    regex = r"(?i)(производитель|изготовитель|поставщик)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'минимальная воспроизводимая частота':
                    regex = r"(?i)(минимальная воспроизводимая частота|минимальная частота|наименьшая частота)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'максимальная воспроизводимая частота':
                    regex = r"(?i)(максимальная воспроизводимая частота|максимальная частота|наибольшая частота)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)


                elif key == 'дисплей':
                    if text.lower().find('дисплей') != -1:
                        characteristics[key] = True

                elif key == 'мощность':
                    regex = r"(?i)(мощность)\s*[:\-]?\s*([^\s\.:]*[^!\?\.,;:])"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'напряжение':
                    regex = r"(?i)напряжение[\s:-]+(?:\S+\s+){0,2}?([^\s\.:><!?;,a-zA-Z]+).*?"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'Комплектация':
                    regex = r"(?i)(?:комплектация|комплекте|набор)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'программы':
                    regex = r"(?i)(?:программа|программы|функция|функции)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'Класс энергопотребления':
                    regex = r"(?i)(?:=класс энергопотребления|энергопотребление|класс энергоэффективности|энергоэффективности|энергоэффективность)[\s:-]+([a-z]+\+*)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'объем':
                    regex = r"(?i)(?:=габариты|объем|величина|размер|размеры)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'конфорки':
                    regex = r"(?i)(?:=конфорки|конфорок|конфорка)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'температура':
                    regex = r"(?i)(?:=температура|температуры|максимальная температура|минимальная температура)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        if word == 'минимальная температура' or word == 'максимальная температура':
                            characteristics[word] = match.group(1)
                        else:
                            characteristics[key] = match.group(1)

                elif key == 'уровень шума':
                    regex = r"(?i)(?:=уровень шума|шум|шумы)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'кол-во полок':
                    regex = r"(?i)(?:=кол-во полок|количествово полок|полки|полок)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'тип сушки':
                    regex = r"(?i)(?:=тип сушки|обсушки|обсушивание|сушка|высушивание)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'потребление воды':
                    regex = r"(?i)(?:=потребление воды|расход воды|использование воды|водопотребление)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'тип нагревательного элемента':
                    regex = r"(?i)(?:=тип нагревательного элемента|нагревательный элемент|нагреватель|термоэлемент|нагревательная спираль)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'рабочая поверхность':
                    regex = r"(?i)(?:=рабочая поверхность|рабочая зона|поверхность)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'количество отделений':
                    regex = r"(?i)(?:=количество отделений|отделений|отделения)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'количество тостов':
                    regex = r"(?i)(?:=количество тостов|число тостов|кол-во тостов)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'автоотключение':
                    regex = r"(?i)(?:=автоотключение|автоматическое отключение|автоматическое выключение|автоматическая остановка)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'степень обжарки':
                    regex = r"(?i)(?:=степень обжарки|степени обжарки|степеней обжарки)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'трафарет':
                    regex = r"(?i)(?:=трафарет)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'регулировка термостата':
                    regex = r"(?i)(?:=регулировка термостата|термостат|регулировка температур)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'автослив масла':
                    regex = r"(?i)(?:=автослив масла|автослив|автоматического слива|дренаж масла|автоматический сливной|автоматический отвод)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'поддержание температуры':
                    regex = r"(?i)(?:=поддержание температуры|поддержка температуры|контроль температуры|поддержание заданной температуры|термоконтроль)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'лимит веса':
                    regex = r"(?i)(?:=лимит веса|ограничение веса|максимальный вес|допустимый вес|допустимая масса|грузовой предел|грузоподъемност)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'точность взвешивания':
                    regex = r"(?i)(?:=трафарет|точность измерения|точность весов)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'тип батареи':
                    regex = r"(?i)(?:=тип батареи|тип аккумулятора|тип питания)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'скорость вращения барабана':
                    regex = r"(?i)(?:=скорость вращения|скорость оборота|скорость кручения|максимальная скорость)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'тип сушки':
                    regex = r"(?i)(?:=тип сушки|вид сушки|метод сушки|технология сушки|режим сушки)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'резюрвар для воды':
                    regex = r"(?i)(?:=резюрвар для воды|резервуар для хранения вод|водный резервуар|бак для воды|емкость для воды)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'автоотчистка':
                    regex = r"(?i)(?:=автоотчистка|автоматическая очистка|автоматической чистки|автоматическая система чистки|самоочистка)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'тип уборки':
                    regex = r"(?i)(?:=тип уборки|метод уборки|способ уборки|вид уборки|режим уборки|режимы уборки)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'регулятор мощности':
                    regex = r"(?i)(?:=регулятор мощности|контроллер мощност|управление мощностью)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'тип сенсоров':
                    regex = r"(?i)(?:=тип сенсоров|вид сенсоров)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'время работы':
                    regex = r"(?i)(?:=время работы|продолжительность работы|длительность работы|время функционирования|время работы без перерывов)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'время зарядки':
                    regex = r"(?i)(?:=продолжительность зарядки|время зарядки|время полной зарядки)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'способ крепления':
                    regex = r"(?i)(?:=способ крепления|метод крепления|вид крепления|способ закрепления|креплени)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'максимальное давление воды':
                    regex = r"(?i)(?:=максимальное давление воды|предел давления воды|максимальное гидравлическое|водяное давление|максимальное внутреннее давление)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'максимальная производительность':
                    regex = r"(?i)(?:=максимальная производительность|макс производительность|макс. производительность|максимальный уровень производительности|уровень производительности)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'регулировка газа':
                    regex = r"(?i)(?:=регулировка газа|управление подачей газа|регулирование потока газа|регулировка расхода газа|управление расходом газа|регулировка интенсивности газа|регулирование давления газа)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'форма корпуса':
                    regex = r"(?i)(?:=форма корпуса|конструкция корпуса|дизайн корпуса|геометрическая форма)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'тип топлива':
                    regex = r"(?i)(?:=тип топлива|вип топлива|сорт топлива|источник топлива)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'расход топлива':
                    regex = r"(?i)(?:=расход топлива|потребление топлива|расход использования топлива|количество топлива|энергопотребление топлива)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'мощность охлаждения':
                    regex = r"(?i)(?:=мощность охлаждения|охлаждающая способность|эффективность охлаждения|скорость охлаждения)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'мощность обогрева':
                    regex = r"(?i)(?:=мощность обогрева|тепловая мощность|уровень обогрева|скорость обогрева)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'отапливаемая территория':
                    regex = r"(?i)(?:=отапливаемая территория|Зона обогрева|Площадь отопления)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)


                elif key == 'тип челнока':
                    regex = r"(?i)(?:=тип челнока|вид челнока|разновидность челнок|челнок)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)


                elif key == 'регулировка скорости шитья':
                    regex = r"(?i)(?:=регулировка скорости шитья|скорости шитья|скорость шитья|контроль скорости|регулировка скорости)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'двойная игла':
                    regex = r"(?i)(?:=двойная игла|двойной иглы|две иглы|параллельная игла|двойной шовная|двойной швейный|двойной стежок|двойная нить)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'защита от перегрева':
                    regex = r"(?i)(?:=защита от перегрева|защита от темп|контроля температур|контроль температур|термическая защита)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)


                elif key == 'насадки':
                    regex = r"(?i)(?:=насадки|насадк|адаптер)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'время для нагрева':
                    regex = r"(?i)(?:=время для нагрева|время нагрева|скорость нагрева)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'cамозатачивающиеся ножи':
                    regex = r"(?i)(?:=самозатачивающиеся ножи|самозатачивающиеся|автоматически затачивающиеся|затачивающ|автозатач)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'материал лезвий':
                    regex = r"(?i)(?:=материал лезвий|лезвия из|лезвие из|лезвие состоит)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'общее число мегапикселей матрицы':
                    regex = r"(?i)(?:=общее число мегапикселей матрицы|разрешение матрицы|матрицы в мегапикселях|пикселей на матрице)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'число эффективных мегапикселей':
                    regex = r"(?i)(?:=число эффективных мегапикселей|эффективных мегапикселей|эффективные мегапиксели)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'тип матрицы':
                    regex = r"(?i)(?:=тип матрицы|вид матрицы|разновидность матрицы)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'кроп фактор':
                    regex = r"(?i)(?:=кроп фактор|фактор кадрирования|коэффициент обрезки|кроп-фактор)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'максимальное разрешение':
                    regex = r"(?i)(?:=максимальное разрешение|наибольшее разрешение|максимальное число пикселей|максимальное количество пикселей|максимальное число точек)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'количество объективов':
                    regex = r"(?i)(?:=количество объективов|кол-во объективов|объективы|дополнительный объектив|дополнительные объективы)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'фокусное расстояние':
                    regex = r"(?i)(?:=фокусное расстояние|расстояние до фокуса|оптическое фокусное|фокусное)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'значение диафрагмы':
                    regex = r"(?i)(?:=значение диафрагмы|диафрагмальное отверстие|бленда|диафрагмальный затвор|регулятор диафрагмы)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'выдержка':
                    regex = r"(?i)(?:=выдержка|скорость затвора|время экспозиции|затворная скорость|время выдержки|длительность экспозиции)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'форматы фотографий':
                    regex = r"(?i)(?:=форматы фотографий|поддерживающие форматы|форматы изображений|форматы)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'поддержка 4К':
                    regex = r"(?i)(?:=поддержка 4К|поддержка 2160p|воспроизведение 4K-видео|поддержка 4K-разрешения|4K-совместимость)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'поддержка full hd':
                    regex = r"(?i)(?:=поддержка full hd|поддержка 1080p|воспроизведение full hd|поддержка full hd разрешения|full hd совместимость)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'процессор':
                    regex = r"(?i)(?:=процессор|cpu|центральный процессор|микропроцессор|ЦПУ)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'угол обзора':
                    regex = r"(?i)(?:=угол обзора|угол зрения|угол видимости|угол наблюдения|угол поля зрения)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'стабилизация картинки':
                    regex = r"(?i)(?:=стабилизация картинки|антидрожание изображения|антидрожание|стабилизации изображения|стабилизация изображения|технология снижения вибрации)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)


                elif key == 'форматы видео':
                    regex = r"(?i)(?:=форматы видео|поддерживающие форматы видео|форматы видеосъемки)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'цокль':
                    regex = r"(?i)(?:=цокль|гнездо|цокл|разъем)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[word] = match.group(1)

                elif key == 'цвет лампочки':
                    regex = r"(?i)(?:=цвет лампочки|цвет стекла|цвет)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[word] = match.group(1)

                elif key == 'цвет света':
                    regex = r"(?i)(?:=цвет света|цветовая температура|оттенок света|цветовой оттенок)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[word] = match.group(1)

                elif key == 'срок службы':
                    regex = r"(?i)(?:=срок службы|время эксплуатации|рабочий период)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[word] = match.group(1)

                elif key == 'колличество источников света':
                    regex = r"(?i)(?:=колличество источников света|колличество ламп|число источников освещения|количество светильников)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'максимальная освещаемая территория':
                    regex = r"(?i)(?:=максимальная освещаемая территория|площадь освещения|площадь охватываемая|покрытие светом)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'пульсация':
                    regex = r"(?i)(?:=пульсация|мерцание света|фликеринг|сверкание света|переменное освещение)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'диапозон рабочих температур':
                    regex = r"(?i)(?:=диапозон рабочих температур|рабочий температурный диапазон|диапазон рабочих условий|рабочий диапазон температур|диапазон температур эксплуатации)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'внутренние габариты':
                    regex = r"(?i)(?:=внутренние габариты|внутренние размеры|внутренние размеры корпуса|внутренние размеры устройства|внутренний объем)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'колличество кнопок':
                    regex = r"(?i)(?:=колличество кнопок|колличество переключатей|колличество клавиш)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'номинальный ток':
                    regex = r"(?i)(?:=номинальный ток|рейтинговый ток|номинальный электрический ток|допустимый ток|максимальный ток|электрическая нагрузка|допустимая мощность|нагрузочная способность)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'гнезда':
                    regex = r"(?i)(?:=гнезда|контакты розеток|электрические контакты|контактные гнезда|розеточные гнезда|электрические выводы|контактные зоны)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'полоса частот':
                    regex = r"(?i)(?:=полоса частот|частотный диапазон|рабочий диапазон частот|диапазон частотной характеристики|диапазон частотных колебаний|частотный спектр)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'разрешение печати':
                    regex = r"(?i)(?:=разрешение печати|качество печати|точность печати|детализация печати|плотность точек)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'скорость печати':
                    regex = r"(?i)(?:=скорость печати|темп печати|быстрота набора|скорость набора|скорость набора текста)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'технология подключения':
                    regex = r"(?i)(?:=технология подключения|методы подключения|техника подключения|способы подключения|поддерживаемые способы подключения)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'двусторонняя печать':
                    regex = r"(?i)(?:=двусторонняя печать|двухсторонняя печать|двойная печать|печать на обеих|двухсторонний вывод)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'поддерживаемые форматы бумаг':
                    regex = r"(?i)(?:=поддерживаемые форматы бумаг|форматы бумаг|формат бумаг|размеры бумаг|размеры листов|типы бумаг)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'технологии печати':
                    regex = r"(?i)(?:=технологии печати|технологии лазерной печати|технология печати)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'цветная печать':
                    regex = r"(?i)(?:=цветная печать|печать в цвете|цветной вывод|цветопечать|полноцветная печать)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'поддерживаемая плотность носителей':
                    regex = r"(?i)(?:=поддерживаемая плотность носителей|допустимая плотность|плотность)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'кол-во игроков':
                    regex = r"(?i)(?:=кол-во игроков|количество игроков|количество участников|число игроков|количество играющих|число участников)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'время игры':
                    regex = r"(?i)(?:=время игры|продолжительность игры|длительность игры|время проведения игры)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'язык игры':
                    regex = r"(?i)(?:=язык игры|язык|локализация|перевод на)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)


                elif key == 'материал на ощупь':
                    regex = r"(?i)=?(материал на ощупь|ткань|мягкая|пластик|плюш|резин)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(1) + ' ' + match.group(2)

                elif key == 'ограничения по возрасту':
                    regex = r"(?i)(?:=ограничения по возрасту|возрастные ограничения|рекомендуемый возраст)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'жанр':
                    regex = r"(?i)(?:=жанр|жанровость)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)


                elif key == 'безопастность':
                    regex = r"(?i)(?:=безопастность)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'проводник':
                    regex = r"(?i)(?:=проводник)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'изоляция':
                    regex = r"(?i)(?:=изоляция)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'экран':
                    regex = r"(?i)(?:=экран|экран провода|экранирование проводов|экранирование)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'электрическое сопротивление':
                    regex = r"(?i)(?:=электрическое сопротивление|электрическая сопротивляемость|электрическая резистивность)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'сопротивление':
                    regex = r"(?i)(рсопротивление|импеданс|электическое сопротивление)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'чувствительность ':
                    regex = r"(?i)(чувствительность|эффективность звук|уровень громкости|звуковая мощность)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'микрофон':
                    regex = r"(?i)(микрофон|есть микрофон|наличие микрофона)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = True
                    else:
                        characteristics[key] = False

                elif key == 'bluetooth':
                    regex = r"(?i)(bluetooth)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = True
                    else:
                        characteristics[key] = False

                elif key == 'способ передачи сигнала':
                    regex = r"(?i)(способ передачи сигнала|технология передачи сигнала|передача сигнала|способ подключения)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'поддержка карты памяти':
                    regex = r"(?i)(поддержка карты памяти|карты памяти|разъем для карт|разъем карт)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = True
                    else:
                        characteristics[key] = False

                elif key == 'принцип работы':
                    regex = r"(?i)(принцип работы|принцип действия|принцип микроф|способ работы)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'колки':
                    regex = r"(?i)(колки|струнодержатели|крепление струн|колк)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'мензура':
                    regex = r"(?i)(мензура|длинна|размер)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'звукосниматель':
                    regex = r"(?i)(звукосниматель|тонозаборник|звукоприемник)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'размер в четвертях':
                    match = re.search(r"\d+/\d+", text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'подбородник':
                    regex = r"(?i)(подбородник|подподкова|подбородная)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'смычок':
                    regex = r"(?i)(смычок|артикуляция|смычк)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'октавы':
                    regex = r"(?i)(октавы|октав|октавный диапазон)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'чувствительность клавиш':
                    regex = r"(?i)(чувствительность клавиш|чувствительность к нажатию|чувствительность нажатия|отзывчивость клав)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'педали':
                    regex = r"(?i)(педали|педаль)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'тембр':
                    regex = r"(?i)(тембр|звуковой окрас|тональность)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'строй':
                    regex = r"(?i)(строй|аккордность|тональность)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'части':
                    regex = r"(?i)(мундштук|трубка-горлышко|корпус инструмента|клапаны|клавиши|звуковая дырка|отверстие|губная пластина|губная дырка|расширительная колба)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'пэд':
                    regex = r"(?i)(пэд|перкуссионные подушки|чинели|чайны|тарелки)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)


                elif key == 'левая рука':
                    regex = r"(?i)(левая рука|левой руке|левая)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'правая рука':
                    regex = r"(?i)(правая рука|правой руке|правая)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)

                elif key == 'регистры':
                    regex = r"(сопрано|меццо-сопрано|контральто|тенор|баритон|бас)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'ряды':
                    regex = r"(?i)(ряды|клавиши|гриф)\s*[:\-]?\s*([^\s\.]+)"
                    match = re.search(regex, text)
                    if match:
                        characteristics[key] = match.group(2)



                elif key == 'рабочее напряжение':
                    regex = r"(?i)(?:=рабочее напряжение|максимальное напряжение)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'стандарт wifi':
                    regex = r"(?i)(?:=стандарт wifi|стандарт беспроводной связи Wi-Fi|Wi-Fi технология|протокол Wi-Fi|спецификация Wi-Fi)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'максимальная скорость интернета':
                    regex = r"(?i)(?:=максимальная скорость интернета|максимальная пропускная способность|скорость передачи данных|максимальная скорость|скорость интернет-соединения)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'диапазоны частот':
                    regex = r"(?i)(?:=диапазоны частот|частотный диапазон|диапазон частотных волн|спектр частот)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                elif key == 'порты':
                    regex = r"(?i)(?:=порты|разъемы|интерфейсы|коннекторы)[\s:-]+([^\.\n]*[A-Z]?).*"
                    match = re.search(regex, text.lower())
                    if match:
                        characteristics[key] = match.group(1)

                break

    return characteristics