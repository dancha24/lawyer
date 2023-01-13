from docxtpl import DocxTemplate
from datetime import datetime, timedelta
import random
import requests
from django.shortcuts import redirect


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


def gen_dog(gen):
    city = gen['city']
    datain = datetime.now() - timedelta(days=random.randint(20, 60))
    dataout = datain.strftime('%d') + '.12.' + datain.strftime('%Y')

    pols = random.randint(0, 1)
    surnameadd = namesand(pols, 1)
    nameadd = namesand(pols, 0)
    datadradd = datetime.now() - timedelta(days=random.randint(12053, 19358))

    iinadd = iingen(datadradd, pols)

    surnameadt = gen['surnameadt']
    nameadt = gen['nameadt']
    patronymicadt = gen['patronymicadt']
    datadradt = gen['datadradt']
    passeradt = gen['passeradt']
    pasnoadt = gen['pasnoadt']
    pasvidanadt = gen['pasvidanadt']
    pascodpadt = gen['pascodpadt']
    pasdataadt = gen['pasdataadt']
    propiskaadt = gen['propiskaadt']

    adress = gen['adress']
    stage = random.randint(1, 5)

    context = {
        'city': city,
        'datain': datain.strftime('%d.%m.%Y'),
        'dataout': dataout,

        'surnameadd': surnameadd,
        'nameadd': nameadd,
        'nameaddk': nameadd[0],
        'datadradd': datadradd.strftime('%d.%m.%Y'),
        'iinadd': iinadd,

        'surnameadt': surnameadt,
        'nameadt': nameadt,
        'nameadtk': nameadt[0],
        'patronymicadt': patronymicadt,
        'patronymicadtk': patronymicadt[0],
        'datadradt': datadradt,
        'passeradt': passeradt,
        'pasnoadt': pasnoadt,
        'pasvidanadt': pasvidanadt,
        'pascodpadt': pascodpadt,
        'pasdataadt': pasdataadt,
        'propiskaadt': propiskaadt,

        'adress': adress,
        'stage': stage,
    }

    # Генерация документов по варианту документа
    doc = DocxTemplate("static/DocTemp/Шаблон аренды Квартиры.docx")  # Подгрузка шаблона Договора
    doc.render(context)
    doc.save("static/DocEx/Аренды Квартиры " + surnameadt + ".docx")
    return redirect("/static/DocEx/Аренды Квартиры " + surnameadt + ".docx")


def gen_sprav(gen):
    datain = datetime.now() - timedelta(days=random.randint(5, 10))

    surnameadt = gen['surnameadt']
    nameadt = gen['nameadt']
    patronymicadt = gen['patronymicadt']
    datadradt = gen['datadradt']
    pols = 0

    iinadd = iingen(datetime.strptime(datadradt, '%d.%m.%Y'), pols)

    adress = gen['adress']
    noschet = str(random.randint(10000, 80000))
    nosprav = str(random.randint(1000, 5000))

    context = {
        'd': datain.strftime('%d'),
        'monthrod': strmonthrod(datain.month),
        'y': datain.year,

        'iinadd': iinadd,

        'surnameadt': surnameadt,
        'nameadt': nameadt,
        'patronymicadt': patronymicadt,
        'noschet': noschet,
        'nosprav': nosprav,

        'adress': adress,
    }

    # Генерация документов по варианту документа
    doc = DocxTemplate("static/DocTemp/Шаблон каспи.docx")  # Подгрузка шаблона Договора
    doc.render(context)
    doc.save("static/DocEx/Готовая справка каспи " + surnameadt + ".docx")
    return redirect("/static/DocEx/Готовая справка каспи " + surnameadt + ".docx")
