from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from .models import Affairs, ExtraPerfomer, ExtraAffairs
from finansy.models import Receipt, Spending
from . import forms
from finansy.forms import ReceiptAddOnAffairForm, SpendingAddOnAffairForm
from django.shortcuts import redirect
from django.db.models import Sum
from performers.models import Performers
# from performers.models import Performers
from datetime import datetime, date


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
        'prise_all': Affairs.prise_all(),
        'customers_debt_all': Affairs.customers_debt_all(),
        'rec_all_affair_sum': Affairs.rec_all_affair_sum(),
        'menu': 'affairs',
        'submenu': 'affairs_all',
        'titlepage': 'Список дел',
    }

    return render(request, 'affairs/affairs_all.html', context)


# Список всех дел по фильтру
@permission_required('affairs.view_affairs', raise_exception=True)  # Проверка прав
def filterfor(request, date_in=date(2021, 5, 1), date_in_max=date(2021, 5, 31), performer_id=8):
    performer = Performers.objects.get(pk=performer_id)

    affairs_all = Affairs.objects.all().filter(date_in__gte=date_in, date_in__lte=date_in_max)
    affairs_per = affairs_all.filter(performer=8)
    affairs = affairs_all.exclude(performer=8)

    extra_per_all = ExtraPerfomer.objects.filter(affairs_id__in=affairs_per.all().values_list('id', flat=True))

    sum_nagrada = extra_per_all.aggregate(Sum('sum'))['sum__sum']
    sum_pay = extra_per_all.aggregate(Sum('payment'))['payment__sum']
    sum_debt = sum_nagrada - sum_pay

    sum_dela_ved = affairs.aggregate(Sum('prise'))['prise__sum']
    for af in affairs_per:
        ex = ExtraAffairs.objects.filter(affairs_id=af.id)
        for e in ex:
            if ExtraPerfomer.objects.get(performer=8, affairs_id=af.id) == ExtraPerfomer.objects.get(performer=8, extraaffairs_id=e.id):
                sum_dela_ved += ExtraPerfomer.objects.get(performer=8, affairs_id=af.id).sum

    suma = affairs.aggregate(Sum('prise'))['prise__sum']
    allrec = 0
    debt = 0
    suma_all = affairs_all.aggregate(Sum('prise'))['prise__sum']
    allrec_all = 0
    debt_all = 0
    for af in affairs:
        debt += af.customers_debt()
        allrec += af.all_rec_sum()
    for af in affairs_all:
        debt_all += af.customers_debt()
        allrec_all += af.all_rec_sum()
    context = {
        'performer': performer,

        'affairs_all': affairs_all,
        'affairs_no': affairs,

        'prise_sum': suma,
        'customers_debt': debt,
        'rec_affair_sum': allrec,

        'prise_sum_all': suma_all,
        'customers_debt_all': debt_all,
        'rec_affair_sum_all': allrec_all,

        'sum_nagrada': sum_nagrada,
        'sum_pay': sum_pay,
        'sum_debt': sum_debt,
        'sum_dela_ved': sum_dela_ved,
        'sum_dela_pro': sum_dela_ved / 100 * 5,
        'sum_dela_ved_pe': sum_debt,
        'menu': 'affairs',
        'submenu': 'affairs_all',
        'titlepage': 'Отчет по главному юристу ' + performer.fio_min(),
    }

    return render(request, 'affairs/affairs_filterfor.html', context)


# Добавление дела
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
    extra_affairs = ExtraAffairs.objects.filter(affairs_id=affair_id)  # Дополнительные дела
    # изменение вознаграждения в промежутке
    if 'performer_sum' in request.POST and request.POST['performer_sum']:
        y = affair.affair_performers().get(performer_id=request.POST['performer_sum_id'], affairs_id=affair_id)
        y.sum = request.POST['performer_sum']
        # y.payment = request.POST['kmpred']
        y.save()
        return redirect('affairs_info', affair_id=affair_id)
    # изменение оплаты в промежутке
    if 'performer_payment' in request.POST and request.POST['performer_payment']:
        y = affair.affair_performers().get(performer_id=request.POST['performer_payment_id'], affairs_id=affair_id)
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
    if 'dop_add' in request.POST and request.POST['dop_add']:
        form_dop = forms.ExtraAffairsAddOnAffairsForm(request.POST, request.FILES)
        if form_dop.is_valid():
            send = form_dop.save(commit=False)
            send.affairs = affair
            send.save()
            return redirect('affairs_info', affair_id=affair_id)
    else:
        form_dop = forms.ExtraAffairsAddOnAffairsForm(initial={'affairs': affair})
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
        'form_rec': form_rec,
        'form_spe': form_spe,
        'form_dop': form_dop,
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
            form.save_m2m()
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


# Добавление доп. дела
@permission_required('affairs.add_extraaffairs', raise_exception=True)
def extra_affairs_add(request):
    if request.method == "POST":
        form = forms.ExtraAffairsAddForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            if 'add' in request.POST and request.POST['add']:
                return redirect('extra_affairs_add')
            else:
                return redirect('extra_affairs_info', extra_affairs_id=form.save().id)
    else:
        form = forms.ExtraAffairsAddForm()
    context = {
        'menu': 'affairs',
        'submenu': 'extra_affairs_all',
        'form': form,
        'titlepage': 'Добавление доп. дела',
    }

    return render(request, 'affairs/affairs_add.html', context)


# Информация об доп.деле
@permission_required('affairs.view_extraaffairs', raise_exception=True)  # Проверка прав
def extra_affairs_info(request, extra_affairs_id):
    extra_affairs = ExtraAffairs.objects.get(pk=extra_affairs_id)
    # изменение вознаграждения в промежутке
    if 'performer_sum' in request.POST and request.POST['performer_sum']:
        y = extra_affairs.ex_affair_performers().get(performer_id=request.POST['performer_sum_id'],
                                                     extraaffairs_id=extra_affairs_id)
        ta = ExtraPerfomer.objects.get(performer_id=request.POST['performer_sum_id'],
                                       affairs_id=extra_affairs.affairs.id)
        ta.sum += int(request.POST['performer_sum']) - y.sum
        ta.save()
        y.sum = request.POST['performer_sum']
        y.save()
        return redirect('extra_affairs_info', extra_affairs_id=extra_affairs_id)
    context = {
        'affair': extra_affairs,
        'menu': 'affairs',
        'submenu': 'extra_affairs_all',
        'titlepage': 'Информация о доп.деле ' + extra_affairs.name,
    }

    return render(request, 'affairs/extra_affairs_info.html', context)


# Изменение записи доп.дела
@permission_required('affairs.change_affairs', raise_exception=True)
def extra_affairs_change(request, extra_affairs_id):
    affair = ExtraAffairs.objects.get(pk=extra_affairs_id)
    if request.method == "POST":
        form = forms.ExtraAffairsAddForm(request.POST, instance=affair)
        if form.is_valid():
            send = form.save(commit=False)
            form.save_m2m()
            send.save()
            return redirect('extra_affairs_info', extra_affairs_id=extra_affairs_id)
    else:
        form = forms.ExtraAffairsAddForm(instance=affair)
    context = {
        'menu': 'affairs',
        'submenu': 'extraaffairs_all',
        'form': form,
        'titlepage': 'Изменение доп.дела ' + str(affair.name),
        'next': False,
    }

    return render(request, 'affairs/affairs_add.html', context)
