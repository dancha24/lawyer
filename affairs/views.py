from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Affairs, ExtraPerfomer, ExtraAffairs
from finansy.models import Receipt, Spending
from . import forms
from finansy.forms import ReceiptAddOnAffairForm, SpendingAddOnAffairForm
from django.shortcuts import redirect
from django.db.models import Sum
# from performers.models import Performers


# Список всех дел
@permission_required('affairs.view_affairs', raise_exception=True)  # Проверка прав
def affairs_all(request):
    affairs = Affairs.objects.all()
    form = forms.AffairsFiltersForm()
    if 'filter' in request.POST:
        response = redirect('affairs_all')
        customers_id = affairs.get(customers=form.fields['customers'])
        response['Location'] += '?customers_id=' + str(customers_id.customers.id)
        return response
    if 'customers_id' in request.GET:
        affairs = affairs.filter(customers=request.GET['customers_id'])
    context = {
        'affairs': affairs,
        'form': form,
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
                return redirect('affairs_info', affair_id=form.save().id)
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
    extra_affairs = ExtraAffairs.objects.filter(affairs_id=affair_id)  # Дополнительные дела
    rec = Receipt.objects.filter(deal_id=affair_id)  # Все доходы
    spe = Spending.objects.filter(deal_id=affair_id)  # Все расходы
    rec_all = 0
    spe_all = 0
    if not not rec:
        rec_all = rec.aggregate(Sum('sum'))['sum__sum']  # Сумма всех доходов
    if not not spe:
        spe_all = spe.aggregate(Sum('sum'))['sum__sum']  # Сумма всех расходов
    # Список промежутков прикрепленных к делу с конкретными исполнителями
    performers_with_prise = ExtraPerfomer.objects.filter(affairs_id=affair_id, performer_id__in=performers_id)
    extra_performers_sum_all = 0
    if not not performers_with_prise:
        # Сумма всех вознаграждений в промежутках
        extra_performers_sum_all = performers_with_prise.aggregate(Sum('sum'))['sum__sum']
    profit_now = rec_all - spe_all
    profit_all = affair.prise - extra_performers_sum_all
    # изменение вознаграждения в промежутке
    if 'performer_sum' in request.POST and request.POST['performer_sum']:
        y = performers_with_prise.get(performer_id=request.POST['performer_sum_id'], affairs_id=affair_id)
        y.sum = request.POST['performer_sum']
        # y.payment = request.POST['kmpred']
        y.save()
        return redirect('affairs_info', affair_id=affair_id)
    # изменение оплаты в промежутке
    if 'performer_payment' in request.POST and request.POST['performer_payment']:
        y = performers_with_prise.get(performer_id=request.POST['performer_payment_id'], affairs_id=affair_id)
        y.payment = request.POST['performer_payment']
        y.save()
        return redirect('affairs_info', affair_id=affair_id)
    # изменение вознаграждения по делу
    if 'priseperformer' in request.POST and request.POST['priseperformer']:
        affair.priseperformer = request.POST['priseperformer']
        affair.save()
        return redirect('affairs_info', affair_id=affair_id)
    if 'rec_add' in request.POST and request.POST['rec_add']:
        form_rec = ReceiptAddOnAffairForm(request.POST)
        if form_rec.is_valid():
            send = form_rec.save(commit=False)
            send.deal = affair
            send.save()
            return redirect('affairs_info', affair_id=affair_id)
    else:
        form_rec = ReceiptAddOnAffairForm()
    if 'spe_add' in request.POST and request.POST['spe_add']:
        form_spe = SpendingAddOnAffairForm(request.POST)
        if form_spe.is_valid():
            send = form_spe.save(commit=False)
            send.deal = affair
            send.save()
            return redirect('affairs_info', affair_id=affair_id)
    else:
        form_spe = SpendingAddOnAffairForm()
    if 'rec_id_del' in request.POST and request.POST['rec_id_del']:
        rec = Receipt.objects.get(id=request.POST['rec_id_del'])
        rec.delete()
        return redirect('affairs_info', affair_id=affair_id)
    if 'spe_id_del' in request.POST and request.POST['spe_id_del']:
        spe = Spending.objects.get(id=request.POST['spe_id_del'])
        spe.delete()
        return redirect('affairs_info', affair_id=affair_id)

    context = {
        'affair': affair,
        'extra_affairs': extra_affairs,
        'performers': performers_with_prise,
        'rec': rec,
        'spe': spe,
        'rec_all': rec_all,
        'spe_all': spe_all,
        'profit_now': profit_now,
        'profit_all': profit_all,
        'form_rec': form_rec,
        'form_spe': form_spe,
        'menu': 'affairs',
        'submenu': 'affairs_all',
        'titlepage': 'Информация о деле ' + affair.name,
    }

    return render(request, 'affairs/affairs_info.html', context)


# Изменение записи дела
@permission_required('affairs.change_affairs', raise_exception=True)
def affairs_change(request, affair_id):
    affair = Affairs.objects.get(pk=affair_id)
    if request.method == "POST":
        form = forms.AffairsAddForm(request.POST, instance=affair)
        if form.is_valid():
            send = form.save(commit=False)
            send.save()
            return redirect('affairs_info', affair_id=affair_id)
    else:
        form = forms.AffairsAddForm(instance=affair)
    context = {
        'menu': 'affairs',
        'submenu': 'affairs_all',
        'form': form,
        'titlepage': 'Изменение дела ' + str(affair.name),
        'next': False,
    }

    return render(request, 'affairs/affairs_add.html', context)


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
