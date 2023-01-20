from docxtpl import DocxTemplate
from datetime import datetime, timedelta
import random
import requests
from django.shortcuts import redirect
from .models import Customers, SpravKaspiVarVipis
from bs4 import BeautifulSoup as bs
from dateutil.parser import parse
from pprint import pprint
from django.db.models import Max
import locale


locale.setlocale(locale.LC_ALL, '')
locale._override_localeconv = {'mon_thousands_sep': '.'}


def locformat(sumap):
    return "{:,.2f}".format(sumap).replace(',', ' ')


def namesand(pol, x):
    otvet = requests.post("https://randomall.ru/api/gens/5437").json()['msg']
    name = str(otvet).replace('.', '').replace('(Женское) ', '').replace(';', '').replace('(Мужское) ', '')
    return name.split('\n')[pol].split(' ')[x]


def strmonthrod(month):
    mon = ['0', 'Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
           'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря', ]
    return mon[month]


def iingen(dr, pol):
    sryaz = 0
    peyaz = dr.strftime('%Y')[2:4] + dr.strftime('%m') + dr.strftime('%d')
    if int(dr.year) < 1900:  # родившихся в XIX веке
        if pol == 0:  # Мужчины
            sryaz = 1
        else:
            sryaz = 2
    if 2000 > int(dr.year) > 1900:  # родившихся в XX веке
        if pol == 0:  # Мужчины
            sryaz = 3
        else:
            sryaz = 4
    if int(dr.year) > 2000:  # родившихся в XXI веке
        if pol == 0:  # Мужчины
            sryaz = 5
        else:
            sryaz = 6
    return peyaz + str(sryaz) + str(random.randint(1000, 5000)) + str(random.randint(1, 9))


def dataingen(x, y):
    weekday = 6
    dataa = datetime.now()
    while weekday == 6 or weekday == 5:
        dataa = datetime.now() - timedelta(days=random.randint(x, y))
        weekday = dataa.weekday()
    return dataa


def savedoc(temp, context):
    fulldocname = "static/DocEx/" + context['namedoc'] + ".docx"
    doc = DocxTemplate(temp)  # Подгрузка шаблона Договора
    doc.render(context)
    doc.save(fulldocname)
    return redirect('/' + fulldocname)


def get_exchange_list_xrates(currency, amount=1, target=None):
    # make the request to x-rates.com to get current exchange rates for common currencies
    content = requests.get(f"https://www.x-rates.com/table/?from={currency}&amount={amount}").content
    # initialize beautifulsoup
    soup = bs(content, "html.parser")
    # get the last updated time
    price_datetime = parse(soup.find_all("span", attrs={"class": "ratesTimestamp"})[1].text)
    # get the exchange rates tables
    exchange_tables = soup.find_all("table")
    exchange_rates = {}
    for exchange_table in exchange_tables:
        for tr in exchange_table.find_all("tr"):
            # for each row in the table
            tds = tr.find_all("td")
            if tds:
                currency = tds[0].text
                # get the exchange rate
                exchange_rate = float(tds[1].text)
                exchange_rates[currency] = exchange_rate
    if target is not None:
        return exchange_rates[target]
    else:
        return price_datetime, exchange_rates


def get_random_vipis():
    max_id = SpravKaspiVarVipis.objects.all().aggregate(max_id=Max("id"))['max_id']
    while True:
        pk = random.randint(1, max_id)
        category = SpravKaspiVarVipis.objects.filter(pk=pk).first()
        if category:
            return category


def gen_dog_arenda(customer_id):
    customer = Customers.objects.get(pk=customer_id)
    datain = dataingen(20, 60)

    pols = random.randint(0, 1)
    nameadd = namesand(pols, 0)
    datadradd = datetime.now() - timedelta(days=random.randint(12053, 19358))

    adress = customer.adresfiktiv
    stage = random.randint(1, 5)

    context = {
        'city': customer.cityfiktiv,
        'datain': datain.strftime('%d.%m.%Y'),
        'dataout': datain.strftime('%d') + '.12.' + datain.strftime('%Y'),
        'surnameadd': namesand(pols, 1),
        'nameadd': nameadd,
        'nameaddk': nameadd[0],
        'datadradd': datadradd.strftime('%d.%m.%Y'),
        'iinadd': iingen(datadradd, pols),
        'surnameadt': customer.surname,
        'nameadt': customer.name,
        'nameadtk': customer.name[0],
        'patronymicadt': customer.patronymic,
        'patronymicadtk': customer.patronymic[0],
        'datadradt': customer.dr,
        'pasnoadt': customer.pasno,
        'pasvidanadt': customer.pasby,
        'pascodpadt': customer.paskod,
        'pasdataadt': customer.pasdate,
        'propiskaadt': customer.address,
        'adress': adress,
        'stage': stage,
        'namedoc': 'Договор аренды Квартиры',

    }

    # Генерация документов по варианту документа
    return savedoc("static/DocTemp/Шаблон аренды Квартиры.docx", context)


def gen_sprav_kaspi_one(customer_id):
    customer = Customers.objects.get(pk=customer_id)

    datain = dataingen(2, 5)

    allpas = 'Паспорт № ' + customer.pasno + ' Выдан: ' + customer.pasby + ' Код подразделения ' + customer.paskod + ' Дача выдачи: ' + customer.pasdate.strftime('%d.%m.%Y')
    pols = customer.pol

    iinadd = iingen(customer.dr, pols)

    context = {
        'prover': pols,
        'd': datain.strftime('%d'),
        'monthrod': strmonthrod(datain.month),
        'y': datain.year,

        'iinadd': iinadd,

        'surnameadt': customer.surname,
        'nameadt': customer.name,
        'patronymicadt': customer.patronymic,
        'noschet': str(random.randint(10000, 80000)),
        'nosprav': str(random.randint(1000, 5000)),
        'nork': str(random.randint(1000, 5000)),
        'allpas': allpas,

        'adress': customer.adresfiktiv,
        'namedoc': 'Справка',
    }
    return savedoc("static/DocTemp/Шаблон каспи.docx", context)


def gen_sprav_kaspi_two(customer_id):

    customer = Customers.objects.get(pk=customer_id)
    dataout = dataingen(2, 5)
    datain = dataout - timedelta(days=31)
    pols = customer.pol
    iinadd = iingen(customer.dr, pols)

    pokupki = 0
    sumtenge = random.randrange(80000, 350000, 1000)
    calendar = {}
    datatable = {}
    i = 1
    while i != 21:
        calendar[str(i)] = datain + (dataout - datain) * random.random()
        i += 1
    sorted_values = sorted(calendar.values())  # Sort the values
    sorted_dict = {}

    for i in sorted_values:
        for k in calendar.keys():
            if calendar[k] == i:
                sorted_dict[k] = calendar[k]
                break
    sorted_dict2 = list(sorted_dict.items())

    i = 1
    while i != 21:
        cur = get_random_vipis()
        summatab = random.randrange(int(cur.minprise), int(cur.maxprise), int(cur.krat))
        datatable['datatapb' + str(i)] = sorted_dict2[i-1][1].strftime('%d.%m.%y')
        datatable['summatab' + str(i)] = '- ' + locformat(summatab)
        datatable['poraciatab' + str(i)] = cur.oper
        datatable['detali' + str(i)] = cur.name
        pokupki += summatab
        i += 1
    dostupno = sumtenge + pokupki
    context_now = {
        'dataout': dataout.strftime('%d.%m.%y'),
        'datain': datain.strftime('%d.%m.%y'),
        'd': dataout.strftime('%d'),
        'monthrod': strmonthrod(dataout.month),
        'y': dataout.year,

        'iinadd': iinadd,

        'surnameadt': customer.surname,
        'nameadt': customer.name,
        'patronymicadt': customer.patronymic,

        'noschet': 'KZ29722C0000' + str(random.randint(70000000, 90000000)),
        'nosprav': str(random.randint(1000, 5000)),
        'sumtenge': locformat(sumtenge),
        'sumuds': locformat(get_exchange_list_xrates('KZT', sumtenge, 'US Dollar')),
        'sumeur': locformat(get_exchange_list_xrates('KZT', sumtenge, 'Euro')),
        'focard': str(random.randint(2000, 9800)),
        'poplnenia': locformat(0),
        'perevodi': locformat(0),
        'pokupki': locformat(pokupki),
        'syat': locformat(0),
        'raznoe': locformat(0),
        'ostatok': locformat(0),
        'drugoepop': locformat(300000),
        'dostupno': locformat(dostupno),

        'adress': customer.adresfiktiv,
        'namedoc': 'Справка каспи 2',
    }
    context = context_now.copy()  # Copy the dict1 into the dict3 using copy() method
    for key, value in datatable.items():  # use for loop to iterate dict2 into the dict3 dictionary
        context[key] = value
    return savedoc("static/DocTemp/Шаблон каспи 2.docx", context)
