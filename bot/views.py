from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from bot import forms
from django.core.management import call_command
from finansy.models import *
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404
from django.db.models import Sum, Q
# from report.defs import report_receiptspending, report_owe_us, report_car_of_day
import datetime
from datetime import datetime
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView
from bot.models import Promocodes, Botset
from bot import defs


# Список всех промокодов
@permission_required('finansy.add_invoicespaids', raise_exception=True)
def promokods_all(request):
    promokods = Promocodes.objects.select_related()
    context = {
        'titlepage': 'Все промокоды',
        'for_table': promokods,
        'menu': "poker",
        'submenu': "promokods",
    }

    return render(request, 'bot/promokods_all.html', context)

# Добавление Промокода
@permission_required('affairs.add_affairs', raise_exception=True)
def promo_add(request):
    if request.method == "POST":
        form = forms.PromokodAddForm(request.POST)
        if form.is_valid():
            form.save()
            if 'add' in request.POST and request.POST['add']:
                return redirect('promo_add')
            else:
                return redirect('promokodes_all')
    else:
        form = forms.PromokodAddForm()
    context = {
        'menu': 'poker',
        'submenu': 'promokodes',
        'form': form,
        'titlepage': 'Добавление промокода',
    }

    return render(request, 'bot/promoadd.html', context)

# Добавление Промокода
@permission_required('affairs.add_affairs', raise_exception=True)
def promo_edit(request, promo_id):
    promo = Promocodes.objects.get(id=promo_id)
    if request.method == "POST":
        form = forms.PromokodEditForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            if 'add' in request.POST and request.POST['add']:
                return redirect('promo_add')
            else:
                return redirect('promokodes_all')
    else:
        form = forms.PromokodEditForm(instance=promo)
    context = {
        'menu': 'poker',
        'submenu': 'promokodes',
        'form': form,
        'titlepage': 'Редактирование промокода',
    }

    return render(request, 'bot/promoadd.html', context)

# Список всех промокодов
@permission_required('finansy.add_invoicespaids', raise_exception=True)
def botset(request):
    botsets = Botset.objects.select_related()
    # if 'reloadbot' in request.POST and request.POST['reloadbot']:
    #     call_command('bot')
    #     return redirect('botset')
    context = {
        'titlepage': 'Все промокоды',
        'for_table': botsets,
        'menu': "poker",
        'submenu': "promokods",
    }

    return render(request, 'bot/set_all.html', context)

# Добавление Промокода
@permission_required('affairs.add_affairs', raise_exception=True)
def set_edit(request, set_id):
    promo = Botset.objects.get(id=set_id)
    if request.method == "POST":
        form = forms.SetEditForm(request.POST, instance=promo)
        if form.is_valid():
            form.save()
            if 'add' in request.POST and request.POST['add']:
                return redirect('promo_add')
            else:
                return redirect('promokodes_all')
    else:
        form = forms.SetEditForm(instance=promo)
    context = {
        'menu': 'poker',
        'submenu': 'botset',
        'form': form,
        'titlepage': 'Редактирование промокода',
        'next': False,
    }

    return render(request, 'bot/promoadd.html', context)


# Генерация договора аренды жилья
@permission_required('bot.view_botset', raise_exception=True)  # Проверка прав
def gendokaren(request):
    if request.method == "POST":
        form = forms.GendocDorm(request.POST)
        if form.is_valid():
            gen = {
                'surnameadt': request.POST['surnameadt'],
                'nameadt': request.POST['nameadt'],
                'patronymicadt': request.POST['patronymicadt'],
                'datadradt': request.POST['datadradt'],
                'passeradt': request.POST['passeradt'],
                'pasnoadt': request.POST['pasnoadt'],
                'pasvidanadt': request.POST['pasvidanadt'],
                'pascodpadt': request.POST['pascodpadt'],
                'pasdataadt': request.POST['pasdataadt'],
                'propiskaadt': request.POST['propiskaadt'],
                'adress': request.POST['adress'],
                'city': request.POST['city'],
            }
            return defs.gen_dog(gen)
    else:
        form = forms.GendocDorm()

    context = {
        'menu': 'poker',
        'submenu': 'gendokaren',
        'form': form,
        'titlepage': 'Добавление договора по покеру',
        'next': False,
    }
    return render(request, 'bot/gendoc.html', context)


# Генерация справки
@permission_required('bot.view_botset', raise_exception=True)  # Проверка прав
def gensprav(request):
    if request.method == "POST":
        form = forms.GenSpravDorm(request.POST)
        if form.is_valid():
            gen = {
                'surnameadt': request.POST['surnameadt'],
                'nameadt': request.POST['nameadt'],
                'patronymicadt': request.POST['patronymicadt'],
                'datadradt': request.POST['datadradt'],
                'allpas': request.POST['allpas'],
                'adress': request.POST['adress'],
                'pol': request.POST['pol'],
            }
            return defs.gen_sprav(gen)
    else:
        form = forms.GenSpravDorm()

    context = {
        'menu': 'poker',
        'submenu': 'gensprav',
        'form': form,
        'titlepage': 'Добавление справки по покеру',
        'next': False,
    }
    return render(request, 'bot/gendoc.html', context)


# Чарты
def charts(request):
    context = {
        'menu': 'poker',
        'submenu': 'charts',
        'titlepage': 'Чарты',
    }
    return render(request, 'bot/charts.html', context)
