from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Affairs, ExtraPerfomer, ExtraAffairs
from finansy.models import Receipt, Spending
from . import forms
from django.shortcuts import redirect
from django.db.models import Sum
# from performers.models import Performers


# Список всех дел
@permission_required('affairs.view_affairs', raise_exception=True)  # Проверка прав
def affairs_all(request):
    affairs = Affairs.objects.all()
    context = {
        'affairs': affairs,
        'menu': 'affairs',
        'submenu': 'affairs_all',
        'titlepage': 'Список дел',
    }

    return render(request, 'affairs/affairs_all.html', context)


# Добавление записи расхода
@permission_required('affairs.add_affairs', raise_exception=True)
def affairs_add(request):
    if request.method == "POST":
        form = forms.AffairsAddForm(request.POST)
        if form.is_valid():
            form.save()
            if 'add' in request.POST and request.POST['add']:
                return redirect('affairs_add')
            else:
                return redirect('affairs_all')
    else:
        form = forms.AffairsAddForm()
    context = {
        'menu': 'affairs',
        'submenu': 'affairs_all',
        'form': form,
        'titlepage': 'Добавление дела',
    }

    return render(request, 'affairs/affairs_add.html', context)


# Информация об Деле
@permission_required('affairs.view_affairs', raise_exception=True)  # Проверка прав
def affairs_info(request, affair_id):
    affair = Affairs.objects.get(pk=affair_id)
    performers_id = affair.performer.all().values_list('id', flat=True)  # Айдишники исполнителей прикрепленных к делу
    extra_affairs = ExtraAffairs.objects.filter(affairs_id=affair_id)
    rec = Receipt.objects.filter(deal_id=affair_id)
    spe = Spending.objects.filter(deal_id=affair_id)
    if not rec:
        rec_all = 0
    else:
        rec_all = rec.aggregate(Sum('sum'))['sum__sum']
    if not spe:
        spe_all = 0
    # else:
    #     spe_all = spe.aggregate(Sum('sum'))['sum__sum']
    # Список промежутков прикрепленных к делу с конкретными исполнителями
    performers_with_prise = ExtraPerfomer.objects.filter(affairs_id=affair_id, performer_id__in=performers_id)
    extra_performers_sum_all = performers_with_prise.aggregate(Sum('sum'))['sum__sum']
    # profit_now = rec_all - spe_all
    profit_all = affair.prise - extra_performers_sum_all
    context = {
        'affair': affair,
        'extra_affairs': extra_affairs,
        'performers': performers_with_prise,
        'rec': rec,
        'spe': spe,
        'rec_all': rec_all,
        # 'spe_all': spe_all,
        # 'profit_now': profit_now,
        'profit_all': profit_all,
        'menu': 'affairs',
        'submenu': 'affairs_all',
        'titlepage': 'Информация о деле ' + affair.name,
    }

    return render(request, 'affairs/affairs_info.html', context)


# Список всех доп.дел
@permission_required('affairs.view_extraaffairs', raise_exception=True)  # Проверка прав
def extra_affairs_all(request):
    extra_affairs = ExtraAffairs.objects.all()
    context = {
        'extra_affairs': extra_affairs,
        'menu': 'affairs',
        'submenu': 'extra_affairs_all',
        'titlepage': 'Список доп.дел',
    }

    return render(request, 'affairs/extra_affairs_all.html', context)


# Информация об доп.деле
@permission_required('affairs.view_extraaffairs', raise_exception=True)  # Проверка прав
def extra_affairs_info(request, extra_affairs_id):
    extra_affairs = ExtraAffairs.objects.get(pk=extra_affairs_id)
    context = {
        'affair': extra_affairs,
        'menu': 'affairs',
        'submenu': 'extra_affairs_all',
        'titlepage': 'Информация о доп.деле ' + extra_affairs.name,
    }

    return render(request, 'affairs/extra_affairs_info.html', context)
