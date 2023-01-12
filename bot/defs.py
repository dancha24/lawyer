from docxtpl import DocxTemplate
from datetime import datetime, timedelta
import random
import requests
from django.shortcuts import redirect


def namesand(x):
    otvet = requests.post("https://randomall.ru/api/gens/5437").json()['msg']
    name = str(otvet).replace('.', '').replace('(Женское) ', '').replace(';', '').replace('(Мужское) ', '')
    return name.split('\n')[random.randint(0, 1)].split(' ')[x]


def gen_dog(gen):
    city = gen['city']
    datain = datetime.now() - timedelta(days=random.randint(20, 60))
    dataout = datain.strftime('%d') + '.12.' + datain.strftime('%Y')

    surnameadd = namesand(1)
    nameadd = namesand(0)
    datadradd = datetime.now() - timedelta(days=random.randint(12053, 19358))
    iinadd = datadradd.strftime('%Y')[2:4] + datadradd.strftime('%m') + datadradd.strftime('%d') + '3' + str(random.randint(1000, 5000)) + str(random.randint(1, 9))

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
    doc.save("static/DocEx/Аренды Квартиры" + surnameadd + ".docx")
    redirect("/static/DocEx/Аренды Квартиры" + surnameadd + ".docx")
    redirect("/static/DocEx/Аренды Квартиры" + surnameadd + ".docx")
