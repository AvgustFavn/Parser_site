import subprocess

from django.contrib.sessions.backends.db import SessionStore
from django.http import HttpResponse
from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect

from cat.add_prod_module import *
from cat.back import *
from cat.models import *
from cat.parsing_back import update_pic, download_file
from catalog.settings import PASSWORD_UPDATE, BASE_DIR


def index(req):
    return render(req, 'index.html', context={'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req)})


def my_view(request):
    # Преобразование асинхронного представления в синхронное
    return async_to_sync(pars_view)(request)


async def pars_view(req):
    is_admin_ = await async_is_admin(req)
    if is_admin_:
        if req.method == 'GET':
            rows = chars_of_types()
            add_id = 0
            for k, v in rows.items():
                rows[k] = [*v, add_id]
                add_id += 1
            return render(req, 'parsing.html', context={'rows': rows, 'sess': req.session.session_key, 'admin': is_admin_, 'super': async_is_super(req)})
        elif req.method == 'POST':
            res = clear_dict(dict(req.POST))  # dict
            del_keys = []
            typ = None
            for k, v in res.items():
                if k != 'sites':
                    res[k] = v[0]

                if 'False' in v:
                    del_keys.append(k)

                if k == 'тип товара':
                    typ = v[0]
                    q = v[0]
                    if '/' in q:
                        res[k] = q[:q.find('/')]
                    else:
                        res[k] = q

                    print(res[k])

            for el in del_keys:
                del res[el]

            sites = list(res.get("sites", None))[0]
            try:
                prods = res.get("product", None).replace('!', ', ')
            except:
                prods = None
            if res.get('product', None):
                data = {
                    'Загрузка прайсов с сайтов': f'Пользователь запустил пасринг сайтов {sites} для поиска товаров {prods}'}
                await sync_to_async(History.objects.create)(i_c=req.session.get('_auth_user_id'), date_of_change=datetime.today(),
                                       title_prod='Загрузка прайсов с сайтов', done=data)
            else:
                data = {
                    'Загрузка прайсов с сайтов': f'Пользователь запустил пасринг сайтов {sites} для поиска товаров по типу {typ}'}
                await sync_to_async(History.objects.create)(i_c=req.session.get('_auth_user_id'),
                                                            date_of_change=datetime.today(),
                                                            title_prod='Загрузка прайсов с сайтов', done=data)

            await run_pars_all(res.get('sites', None), res.get('product', None), res, req)
            return redirect('/unknows/_1')
    else:
        return redirect('/')

def all_prods(req, page):
    models, caracts = trans_models_carac(reverse=True)
    if req.method == 'GET':
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        rows = get_all_prods()
        rows = list(rows)

        total_items = len(rows)  # Общее количество товаров
        items_per_page = 10  # Количество товаров на странице

        total_pages = int((total_items // items_per_page) + (1 if total_items % items_per_page > 0 else 0))
        page_num = int(page)

        # Определение диапазона страниц для вывода
        num_pages_displayed = 5  # Количество страниц для вывода (5 предыдущих и 5 следующих)
        start_page = max(1, page_num - num_pages_displayed)
        end_page = min(total_pages, page_num + num_pages_displayed) + 1
        pages_range = range(start_page, end_page)

        if page_num == 1:
            rows_for_page = rows[:items_per_page]
            page_prev = None
        else:
            start_index = (page_num - 1) * items_per_page
            end_index = start_index + items_per_page
            rows_for_page = rows[start_index:end_index]
            page_prev = page_num - 1 if page_num - 1 >= 1 else None

        page_next = page_num + 1 if page_num + 1 <= total_pages else None

        last_page = total_pages
        last_minus_six = int(last_page) - 6

        return render(req, 'search_and_prods_test.html', context={
            'rows': rows_for_page,
            'sess': req.session.session_key,
            'total_pages': total_pages,
            'pages_range': pages_range,
            'page_prev': page_prev,
            'page_next': page_next,
            'last_page': int(last_page),
            'admin': is_admin(req),
            'super': is_super(req),
            # 'models': models,
            # 'caracts': caracts,
            'last_minus_six': last_minus_six,
            'page_num': int(page_num)
        })
    
    elif req.method == 'POST':
        prod = req.POST.get('prod')
        chars = dict(req.POST)
        translated_dict = trans_models_carac(reverse=False, chars=chars)
        print(translated_dict.get('yes', 'Никаких ес :('))
        rows = find_prod(prod, translated_dict)

        return render(req, 'search_and_prods_test.html',
                      context={'rows': rows, 'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req), 'models': models, 'caracts': caracts})



def page_prod(req, title):
    prod = find_prod_glob(int(title))
    try:
        prod.price = int(prod.price)
    except:
        pass

    try:
        prod.price_opt = int(prod.price_opt)
    except:
        pass

    chars = {}
    if prod:
        ex = ['name', 'type_of_prod', 'descr', 'pic', 'full_desc', 'price', 'price_opt', 'draft_chars', 'art', 'id']
        list_ = model_to_dict(prod, exclude=ex)
        for k, v in list_.items():
            if v != 'Н.Д.' and v != None:
                chars[k] = v
        chars = update_chars_translate(chars, rus=True)
        print(chars)
        return render(req, 'prod.html', context={'sess': req.session.session_key, 'tup': prod, 'chars': chars, 'idd': title, 'admin': is_admin(req), 'super': is_super(req)})
    return HttpResponse('Не найдена запись товара - чтобы посмотреть ее')


def unk_page_prod(req, title):
    obj = UnknownType.objects.get(id=title)
    if is_admin(req):
        if req.method == 'POST':
            ch = dict()
            ch['categ'] = req.POST['select']
            print(ch)
            model = trans_models_carac(chars=ch, reverse=False)
            print(model)
            model = model['categ']
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            target_model = find_model(model)
            transfer_record_unk(target_model, obj.id)
            do_note_history(req.session.get('_auth_user_id'), title=obj.name, addit_opt=f'смена типа с Без-типового, на {model}')
            return redirect('/unknows/_1')
        else:
            all_models = apps.get_models()
            # models = []
            # for model in all_models:
            #     if model.__name__ not in ['LogEntry', 'Permission', 'Group', 'ContentType', 'Session', 'UnknownType', 'User_my', 'History', 'UniqIdProds']:
            #         models.append(model.__name__)
            models = d.values()
            datass = str(obj.datas)
            try:
                datass = re.sub(r'(\w+)(?=\s*:)(?!файла)', r"'\1'", datass)
                datass = ast.literal_eval(datass)
                datass = update_chars_translate(datass, rus=True)
            except:
                pass
            return render(req, 'change_type_unk.html', context={'sess': req.session.session_key, 'datass': datass, 'obj': obj, 'models': models, 'admin': is_admin(req), 'super': is_super(req)})
    else:
        return redirect('/')

def del_unk(req, title):
    if is_admin(req):
        obj = UnknownType.objects.get(id=title)
        obj.delete()
        do_note_history(req.session.get('_auth_user_id'), title=obj.name, addit_opt='Удаление без-типового товара')
        return redirect('/unknows/_1')
    else:
        return redirect('/')

def is_del_unk(req, title):
    if is_admin(req):
        return render(req, 'del_prod.html', context={'url': f'/unknows/{title}/del_yes', 'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req)})
    else:
        return redirect('/')

def all_unk_prods(req, page):
    if is_admin(req):
        if req.method == 'GET':
            rows = get_all_unk_prods()
            page = int(page)
            if page == 0 or page == 1:
                if len(rows) > 10:
                    rows_for_page = rows[:10]
                else:
                    rows_for_page = rows
                page_prev = None
            else:
                if len(rows) > (int(page) * 10) + 10:
                    rows_for_page = rows[(int(page) - 1 ) * 10:((int(page) - 1 ) * 10) + 10]
                else:
                    rows_for_page = rows[(int(page) - 1 ) * 10:]
                page_prev = int(page) - 1

            if len(rows) < int(page) * 10:
                page_next = None
            else:
                page_next = int(page) + 1

            return render(req, 'unk_prods.html', context={'rows': rows_for_page, 'sess': req.session.session_key, 'page_prev': page_prev, 'page_next': page_next, 'admin': is_admin(req), 'super': is_super(req)})
        elif req.method == 'POST':
            name = req.POST.get('name')
            rows = UnknownType.objects.filter(name__icontains=name)
            return render(req, 'unk_prods.html',
                          context={'rows': rows, 'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req)})

    else:
        return redirect('/')



def reg(req):
    if req.method == 'GET':
        if req.session.session_key != None:
            print(req.session.session_key)
            return redirect('/')
        else:
            return render(req, 'reg.html', context={'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req)})
    elif req.method == 'POST':
        username = req.POST['name']
        password = req.POST['pass_hash']
        email = req.POST['email']
        user = registaration(username, email, password)
        if not user:
            return redirect('/reg')

        session = SessionStore()
        session.create()
        session['user_id'] = user.id
        session.save()

        auth_login(req, user)
        req.session.save()
        return redirect('/')


def login_page(req):
    if req.method == 'GET':
        if req.session.session_key != None:
            return redirect('/')
        else:
            return render(req, 'login.html', context={'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req)})
    elif req.method == 'POST':
        email = req.POST['login']
        password = req.POST['password']
        user = User_my.objects.filter(email=email).first()  # Получить объект пользователя из базы данных
        print(user is not None and is_true_password(password, email))
        if user is not None and is_true_password(password, email):
            session = SessionStore()
            session.create()
            session['user_id'] = user.id
            session.save()
            auth_login(req, user)  # Вход пользователя в систему

            return redirect('/')
        else:
            return render(req, 'login.html', context={'sess': req.session.session_key,
                                                      'error': 'Вы либо не зарегистрированы, либо email или пароль не правильный', 'admin': is_admin(req), 'super': is_super(req)})


def user_page(req):
    return render(req, 'user.html', context={'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req)})


def del_prod(req, title):
    if is_admin(req):
        return render(req, 'del_prod.html', context={'sess': req.session.session_key, 'url': f'/prods/{title}/del_yes', 'admin': is_admin(req), 'super': is_super(req)})
    else:
        return redirect('/')


def del_agreed(req, title):
    if is_admin(req):
        obj = find_prod_glob(int(title))
        if obj:
            model = obj.__class__.__name__
            un = UniqIdProds.objects.filter(native_id=obj.id, model=str(model).lower())
            un.delete()
            obj.delete()
            do_note_history(req.session.get('_auth_user_id'), obj.name, addit_opt='удаление товара')
            return redirect('/prods/_1')

        return HttpResponse('Произошла ошибка при удалении товара')
    else:
        return redirect('/')

def update_prod(req, title):
    if is_admin(req):
        if req.method == 'POST':
            obj = find_prod_glob(int(title))
            id = req.POST.get('id', None)
            pic = req.FILES.get('pic', None)
            name = req.POST.get('name', None)
            full_desc = req.POST.get('full_desc', None)
            price = req.POST.get('price', None)
            price_opt = req.POST.get('price_opt', None)
            select = req.POST.get('select', None)
            select = trans_models_carac(chars={'categ': select}, reverse=False)
            select = select['categ']
            print(select)

            update_fields = {key: value for key, value in req.POST.dict().items() if key.startswith('update_')}
            update_fields = update_chars_translate(update_fields, eng=True)
            a = {}
            select_col = req.POST.get('select_col', None)
            new_val_col = req.POST.get('col_text', None)

            select_col2 = req.POST.get('select_col2', None)
            select_col_b = req.POST.get('select_col_b', None) # True False

            for k, v in update_fields.items():
                k = k[k.find('_') + 1:]
                try:
                    if getattr(obj, k) != v:
                        if k == 'None':
                            k = None
                        elif v == 'None':
                            v = None

                        a[k] = v
                except:
                    pass

            if select_col2 and select_col_b:
                if select_col_b == 'True':
                    a[select_col2] = True
                elif select_col_b == 'False':
                    a[select_col2] = False

            if select_col and new_val_col:
                if select_col != 'N':
                    a[select_col] = new_val_col

            if obj:
                type_table = obj._meta.db_table
                if pic and pic.name != obj.pic:
                    pic_ = update_pic(pic)
                    if pic_:
                        a['pic'] = pic_
                    else:
                        a['pic'] = 'Н.Д.'

                if name and name != obj.name:
                    a['name'] = name

                if full_desc and full_desc != obj.descr:
                    a['descr'] = full_desc

                if price and price != obj.price and price != 'None':
                    a['price'] = float(price)

                if price_opt and price_opt != obj.price and price_opt != 'None':
                    a['price_opt'] = float(price_opt)



                ModelClass = find_model(type_table)
                if ModelClass is not None:
                    model = str(ModelClass.__name__)
                    model = d[model]
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    do_note_history(req.session.get('_auth_user_id'), title=obj.name, a_dict=a, olds={'модель': model, 'id': id})
                    loop.run_until_complete(async_update(ModelClass, a, id))
                    time.sleep(7)
                    if select and str(select).lower() != str(ModelClass.__name__).lower():  # Смена типа товара
                        transfer_record(ModelClass, find_model(select), obj.id)
                        new_mod = find_model(select)
                        new_mod = str(new_mod.__name__)
                        new_mod = d[new_mod]
                        do_note_history(req.session.get('_auth_user_id'), title=obj.name, addit_opt=f'смена типа с {model} на {new_mod}', olds={'модель': ModelClass, 'id': id})

                return redirect('/prods/_1')


            else:
                return HttpResponse('Не найдена запись товара - чтобы изменить ее ')

            return redirect('/prods/_1')

        elif req.method == 'GET':
            obj = find_prod_glob(int(title))
            char_fields = []
            boolean_fields = []

            ex = ['name', 'type_of_prod', 'descr', 'pic', 'full_desc', 'price', 'draft_chars', 'art', 'id']
            chars = model_to_dict(obj, exclude=ex)
            chars = update_chars_translate(chars, rus=True)
            model_name = obj.__class__.__name__
            model_name = d[model_name]
            models = d.values()

            if model_name:
                return render(req, 'change_prod.html',
                              context={'sess': req.session.session_key, 'obj': obj, 'types': models, 'chars': chars, 'model': model_name, 'idd': title,
                                       'columns': not_second_columns(char_fields),
                                       'columns_b': not_second_columns(boolean_fields), 'admin': is_admin(req), 'super': is_super(req)})
            else:
                return HttpResponse('Не найдена запись товара - чтобы изменить ее ')
    else:
        redirect('/')

def is_del_all_unknown(req, page):
    if is_admin(req):
        return render(req, 'del_all_prod.html', context={'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req)})
    else:
        return redirect('/')

def del_all_unknown(req, page):
    if is_admin(req):
        UnknownType.objects.all().delete()
        do_note_history(req.session.get('_auth_user_id'), addit_opt='удаление всех неизвестных типов-товаров')
        return redirect('/unknows/_1')
    else:
        return redirect('/')

def history(req):
    if is_admin(req):
        all = History.objects.all().order_by('-id')
        for r in all:
            for model in apps.get_models():
                if any(isinstance(field, models.CharField) and field.name == 'name' for field in model._meta.get_fields()):
                    obj = model.objects.filter(name=r.title_prod).first()
                    if obj:
                        try:
                            r.pic_title = obj.pic
                        except:
                            r.pic_title = 'Н.Д.'
                        break

            user = User_my.objects.filter(name=r.i_c).first()
            try:
                r.pic_user = user.img
            except:
                r.pic_user = 'Н.Д.'
        return render(req, 'history.html', context={'sess': req.session.session_key, 'rows': all, 'admin': is_admin(req), 'super': is_super(req)})
    else:
        return redirect('/')

def run_do_pars_price(name, prov, user):
    # venv_python = '/home/rdp-user/Desktop/catalog_site/myenv/bin/python3.9'  # Путь к интерпретатору Python в вашем venv на Windows
    venv_python = 'C:\\Users\\avgus\\Documents\\py_shit\\catalog_site\\venv\\Scripts\\python.exe'
    file_path = os.path.join(BASE_DIR, 'cat/do_pars_price.py')

    subprocess.Popen([venv_python, file_path, name, prov, user])

def load_prices(req):
    if is_admin(req):
        if req.method == 'GET':
            all = Providers.objects.all()
            return render(req, 'prices.html', context={'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req), 'all': all})
        elif req.method == 'POST':
            f = req.FILES.get('file_1', None)
            prov_value = next(value for key, value in req.POST.items() if key.startswith('prov_'))
            if f:
                name = download_file(f)
                run_do_pars_price(name, prov_value, req.session.get('_auth_user_id'))
            return redirect('/prods/_1')
    else:
        return redirect('/')


def change_pass(req):
    if req.method == 'GET':
        return render(req, 'change_pas.html', context={'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req)})
    else:
        email = req.POST.get('email', None)
        password = req.POST.get('password', None)
        key = req.POST.get('key', None)
        if email and password and key:
            if key == PASSWORD_UPDATE:
                user = User_my.objects.filter(email=email).exists()
                if user:
                    user = User_my.objects.filter(email=email).first()
                    hash_object = hashlib.sha256()
                    hash_object.update(password.encode('utf-8'))
                    hash_pass = hash_object.hexdigest()
                    user.pass_hash = hash_pass
                    user.save()
                    return redirect('/login')

        return render(req, 'change_pas.html', context={'sess': req.session.session_key, 'error': True, 'admin': is_admin(req), 'super': is_super(req)})

def admin_panel(req):
    if req.method == 'GET':
        super_, admins, users = get_users()
        return render(req, 'admin_panel.html', context={'sess': req.session.session_key, 'super_': super_, 'admins': admins, 'users': users, 'admin': is_admin(req), 'super': is_super(req)})
    else:
        email = req.POST.get('email', None)
        stat = req.POST.get('status', None)
        user = User_my.objects.filter(email=email).first()
        user.status = stat
        user.save()
        return redirect('/admin_panel')

def all_providers(req):
    all = Providers.objects.all()
    return render(req, 'providers.html', context={'all': all, 'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req)})

def update_prov(req, id):
    if req.method == 'POST':
        prov = Providers.objects.get(id=id)
        name_prov = req.POST.get('name', None)
        name_prod = req.POST.get('name_prod', None)
        art = req.POST.get('art', None)
        roz = req.POST.get('roz', None)
        opt = req.POST.get('opt', None)
        descr = req.POST.get('descr', None)
        edge = req.POST.get('edge', None)
        edge_m = req.POST.get('edge_mos', None)
        edge_i = req.POST.get('edge_irk', None)
        edge_n = req.POST.get('edge_nov', None)
        pic = req.POST.get('pic', None)
        id_prov = req.POST.get('id_prov', None)
        free = req.POST.get('free', None)

        if id_prov:
            if name_prov:
                prov.name = name_prov
            if name_prod:
                prov.col_name_prod = name_prod
            else:
                return HttpResponse('Неизвестна колонка для имени товара')
            if art:
                prov.col_art = art
            if roz:
                prov.col_retail_price = roz
            if opt:
                prov.col_wholesale_price = opt
            if descr:
                prov.col_descr = descr
            if edge:
                prov.col_edge = edge
            if edge_m:
                prov.col_edge_mosc = edge_m

            if edge_i:
                prov.col_edge_irk = edge_i
            if edge_n:
                prov.col_edge_novos = edge_n
            if pic:
                prov.col_pic = pic

            if free:
                prov.col_free = free
        else:
            return HttpResponse('Неизвестный поставщик (вероятно вы трогали колонку id)')

        prov.save()
        return redirect(f'/providers/{id}/')
    else:
        prov = Providers.objects.get(id=id)
        return render(req, 'update_provider.html', context={'prov': prov, 'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req)})

def delete_provider(req, id):
    prov = Providers.objects.get(id=id)
    prov.delete()
    return redirect(f'/providers/')

def create_provider(req):
    if req.method == 'GET':
        return render(req, 'update_provider.html', context={'create': True, 'sess': req.session.session_key, 'admin': is_admin(req), 'super': is_super(req)})
    else:
        name_prov = req.POST.get('name', None)
        name_prod = req.POST.get('name_prod', None)
        art = req.POST.get('art', None)
        roz = req.POST.get('roz', None)
        opt = req.POST.get('opt', None)
        descr = req.POST.get('descr', None)
        edge = req.POST.get('edge', None)
        edge_m = req.POST.get('edge_mos', None)
        edge_i = req.POST.get('edge_irk', None)
        edge_n = req.POST.get('edge_nov', None)
        pic = req.POST.get('pic', None)
        sale = req.POST.get('sale', None)
        free = req.POST.get('free', None)
        dd = {}

        if name_prov:
            dd['name'] = name_prov
        if name_prod:
            dd['col_name_prod'] = name_prod
        else:
            return HttpResponse('Неизвестна колонка для имени товара')
        if art:
            dd['col_art'] = art
        if roz:
            dd['col_retail_price'] = roz
        if opt:
            dd['col_wholesale_price'] = opt
        if descr:
            dd['col_descr'] = descr
        if edge:
            dd['col_edge'] = edge
        if edge_m:
            dd['col_edge_mosc'] = edge_m
        if edge_i:
            dd['col_edge_irk'] = edge_i
        if edge_n:
            dd['col_edge_novos'] = edge_n
        if pic:
            dd['col_pic'] = pic
        if sale:
            dd['col_sale'] = sale
        if free:
            dd['col_free'] = free

        Providers.objects.create(**dd)
        return redirect(f'/providers/')