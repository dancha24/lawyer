from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required, permission_required
from bot import forms
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
from bot.models import Promocodes


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
    promokods = Promocodes.objects.select_related()
    context = {
        'titlepage': 'Все промокоды',
        'for_table': promokods,
        'menu': "poker",
        'submenu': "promokods",
    }

    return render(request, 'bot/promokods_all.html', context)