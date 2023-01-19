from docxtpl import DocxTemplate
from datetime import datetime, timedelta
import random
import requests
from django.shortcuts import redirect
from .models import Customers
from docx2pdf import convert
# import os
# import win32com.client


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
    doc = DocxTemplate(temp)  # Подгрузка шаблона Договора
    doc.render(context)
    fulldocname = "static/DocEx/" + context['namedoc']
    doc.save(fulldocname + ".docx")
    # wdFormatPDF = 17
    # inputFile = os.path.abspath(fulldocname + ".docx")
    # outputFile = os.path.abspath(fulldocname + ".pdf")
    # word = win32com.client.Dispatch('Word.Application')
    # doc = word.Documents.Open(inputFile)
    # doc.SaveAs(outputFile, FileFormat=wdFormatPDF)
    # doc.Close()
    # word.Quit()
    convert(fulldocname.replace("/", "\\") + ".docx", fulldocname + ".pdf")
    # convert("static\DocEx\Справка.docx")
    return redirect(fulldocname + ".pdf")


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
