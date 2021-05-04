from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from finansy import forms
from django.shortcuts import redirect
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

from django import template

# Create your views here.
# Список всего прихода
# @permission_required('finansy.add_invoicespaids', raise_exception=True)
from performers.models import Performers



# Добавление записи прихода
@permission_required('finansy.add_invoicespaids', raise_exception=True)
def receipt_add(request):
    if request.method == "POST":
        form = forms.ReceiptForm(request.POST)
        if form.is_valid():
            form.save()
            if 'add_rec' in request.POST and request.POST['add_rec']:
                return redirect('receipt_add')
            if 'add_spe' in request.POST and request.POST['add_spe']:
                return redirect('spending_add')
            else:
                return redirect('finansy_today_period')
    else:
        form = forms.ReceiptForm()
    context = {
        'titlepage': 'Добавление записи прихода',
        'form': form,
    }

    return render(request, 'finansy/add_receipt.html', context)



# Удаление записи прихода
def receipt_del(uid):
    for_del = Receipt.objects.get(id=uid)
    for_del.delete()



# Редактировать Запись прихода
@permission_required('finansy.add_invoicespaids', raise_exception=True)
def receipt_edit(request, receipt_id):
    rec = Receipt.objects.get(pk=receipt_id)

    data = {"sum": rec.sum,
            "date": rec.date}

    if request.method == "POST":
        form = forms.ReceiptForm(request.POST, initial=data)
        if form.is_valid():
            rec.delete()
            form.save()
        return redirect('finansy_today_all')
    else:
        form = forms.ReceiptForm(initial=data)
    context = {
        'titlepage': 'Добавление записи',
        'form': form,
        'next': False,
    }

    return render(request, 'finansy/add_receipt.html', context)


# ????
@permission_required('finansy.add_invoicespaids', raise_exception=True)
def receipt_info(request):
    context = {
        'titlepage': '????',
    }

    return render(request, 'finansy/zp.html', context)



# Добавление записи расхода
@permission_required('finansy.add_invoicespaids', raise_exception=True)
def spending_add(request):
    if request.method == "POST":
        form = forms.SpendingForm(request.POST)
        if form.is_valid():
            form.save()
            if 'add_rec' in request.POST and request.POST['add_rec']:
                return redirect('receipt_add')
            if 'add_spe' in request.POST and request.POST['add_spe']:
                return redirect('spending_add')
            else:
                return redirect('finansy_today_period')
    else:
        form = forms.SpendingForm()
    context = {
        'titlepage': 'Добавление записи расхода',
        'form': form,
    }

    return render(request, 'finansy/add_spending.html', context)


# Список всего расхода
@permission_required('finansy.add_invoicespaids', raise_exception=True)
def spending_all(request):
    spending = Spending.objects.select_related()
    context = {
        'titlepage': 'Записи расхода',
        'for_table': spending,
        'variant': "spending_all",
    }

    return render(request, 'finansy/receiptspending_all.html', context)


# Список всех смен
@permission_required('finansy.add_invoicespaids', raise_exception=True)
def spending_info(request):
    context = {
        'titlepage': '????',
    }

    return render(request, 'finansy/zp.html', context)


# Удаление записи расхода
def spending_del(uid):
    for_del = Spending.objects.get(id=uid)
    for_del.delete()


# Редактировать Запись прихода
@permission_required('finansy.add_invoicespaids', raise_exception=True)
def spending_edit(request, spending_id):
    spe = get_object_or_404(Spending, pk=spending_id)

    data = {"user_do": spe.user_do,
            "sum": spe.sum,
            "type": spe.type,
            "category": spe.category,
            "com": spe.com,
            "date": spe.date}

    if request.method == "POST":
        form = forms.SpendingForm(request.POST, initial=data)
        if form.is_valid():
            spe.delete()
            form.save()
            return redirect('finansy_today_all')
    else:
        form = forms.SpendingForm(initial=data)
    context = {
        'titlepage': 'Добавление записи',
        'form': form,
        'next': False,
    }

    return render(request, 'finansy/add_spending.html', context)










def finansy_today_date(request, y=timezone.datetime.now().year, m=timezone.datetime.now().month,
                       d=timezone.datetime.now().day):
    date = str(y) + '-' + str(m) + '-' + str(d)
    receipts = Receipt.objects.select_related().filter(date=date)
    spendings = Spending.objects.select_related().filter(date=date)
    balances = FinansyBalance.objects.select_related()
    balances_kem_nal = balances.get(type='CH').sum
    balances_kem_ya = balances.get(type='BK').sum
    balances_kem_card = balances.get(type='CD').sum

    if request.method == "POST" and 'other' in request.POST:
        trip_start = request.POST['trip-start']
        trip_date = datetime.strptime(trip_start, "%Y-%m-%d")
        # form = forms.DateForm(request.POST)
        if trip_date != date:
            # fa = form.cleaned_data['gaga']
            # date = datetime.datetime.strptime(fa, '%Y-%m-%d')
            y = trip_date.year
            m = trip_date.month
            d = trip_date.day
            return redirect('finansy_today_date', y=y, m=m, d=d)
    else:
        form = forms.DateForm()
    sum_all_rec = receipts.aggregate(Sum('sum'))['sum__sum']
    sum_all_spe = spendings.aggregate(Sum('sum'))['sum__sum']
    if sum_all_rec is None:
        sum_all_rec = 0
    if sum_all_spe is None:
        sum_all_spe = 0
    context = {
        'titlepage': 'Приход/Расход за ' + str(date),
        'for_table': receipts,
        'for_table2': spendings,
        'variant': "finansy_today_all",
        'sum_all_rec': sum_all_rec,
        'sum_all_spe': sum_all_spe,
        'ost_all': sum_all_rec - sum_all_spe,
        'balances_kem_nal': balances_kem_nal,
        'balances_kem_ya': balances_kem_ya,
        'balances_kem_card': balances_kem_card,
        'DateForm': form,
        'y': y,
        'm': m,
        'd': d,
    }
    if request.method == "POST" and 'del_rec' in request.POST:
        uid = request.POST['id']
        # receipt_del(uid)
        return render(request, 'finansy/receiptspending_all.html', context)
    if request.method == "POST" and 'del_spe' in request.POST:
        uid = request.POST['id']
        # spending_del(uid)
        return render(request, 'finansy/receiptspending_all.html', context)

    return render(request, 'finansy/receiptspending_all.html', context)


def finansy_today_period(request, y=timezone.datetime.now().year, m=timezone.datetime.now().month,
                         d=timezone.datetime.now().day, y2=timezone.datetime.now().year,
                         m2=timezone.datetime.now().month,
                         d2=timezone.datetime.now().day):
    date = str(y) + '-' + str(m) + '-' + str(d)
    # date2 = str(y2) + '-' + str(m2) + '-' + str(d2)
    date3 = str(y) + '-' + str(m) + '-' + str(d)
    date4 = str(y2) + '-' + str(m2) + '-' + str(d2)
    receipts = Receipt.objects.select_related().filter(date=date)
    spendings = Spending.objects.select_related().filter(date=date)
    balances = FinansyBalance.objects.select_related()
    balances_kem_nal = balances.get(type='CH').sum
    balances_kem_ya = balances.get(type='BK').sum
    balances_kem_card = balances.get(type='CD').sum

    if request.method == "POST" and 'other' in request.POST:
        trip_start = request.POST['trip-start']
        trip_start2 = request.POST['trip-start2']
        trip_date = datetime.strptime(trip_start, "%Y-%m-%d")
        trip_date2 = datetime.strptime(trip_start2, "%Y-%m-%d")
        date3 = trip_start
        date4 = trip_start2

        if trip_date != date:
            y = trip_date.year
            m = trip_date.month
            d = trip_date.day
            y2 = trip_date2.year
            m2 = trip_date2.month
            d2 = trip_date2.day
            # return redirect('finansy_period', y=y, m=m, d=d, y2=y2, m2=m2, d2=d2)
    else:
        form = forms.DateForm()
    receipts2 = Receipt.objects.select_related().filter(date__range=(date3, date4))
    spendings2 = Spending.objects.select_related().filter(date__range=(date3, date4))
    sum_all_rec = receipts2.aggregate(Sum('sum'))['sum__sum']
    sum_all_spe = spendings2.aggregate(Sum('sum'))['sum__sum']
    if sum_all_rec is None:
        sum_all_rec = 0
    if sum_all_spe is None:
        sum_all_spe = 0
    context = {
        'titlepage': 'Приход/Расход от ' + str(date3) + ' до ' + str(date4),
        'menu': 'finansy',
        'submenu': 'finansy_today_period',
        'for_table': receipts,
        'for_table2': spendings,
        'for_table3': receipts2,
        'for_table4': spendings2,
        'variant': "finansy_today_all",
        'sum_all_rec': sum_all_rec,
        'sum_all_spe': sum_all_spe,
        'ost_all': sum_all_rec - sum_all_spe,
        'balances_kem_nal': balances_kem_nal,
        'balances_kem_ya': balances_kem_ya,
        'balances_kem_card': balances_kem_card,
        'y': y,
        'm': m,
        'd': d,
        'y2': y2,
        'm2': m2,
        'd2': d2,
    }
    if request.method == "POST" and 'del_rec' in request.POST:
        uid = request.POST['id']
        receipt_del(uid)
        return render(request, 'finansy/receiptspending_period.html', context)
    if request.method == "POST" and 'del_spe' in request.POST:
        uid = request.POST['id']
        spending_del(uid)
        return render(request, 'finansy/receiptspending_period.html', context)

    return render(request, 'finansy/receiptspending_period.html', context)


def dealreports(request, y=timezone.datetime.now().year, m=timezone.datetime.now().month,
                d=timezone.datetime.now().day, y2=timezone.datetime.now().year, m2=timezone.datetime.now().month,
                d2=timezone.datetime.now().day, ):
    date = str(y) + '-' + str(m) + '-' + str(d)
    date3 = str(y) + '-' + str(m) + '-' + str(d)
    date4 = str(y2) + '-' + str(m2) + '-' + str(d2)
    if request.method == "POST" and 'other' in request.POST:
        trip_start = request.POST['trip-start']
        trip_start2 = request.POST['trip-start2']
        trip_date = datetime.strptime(trip_start, "%Y-%m-%d")
        trip_date2 = datetime.strptime(trip_start2, "%Y-%m-%d")
        date3 = trip_start
        date4 = trip_start2
        if trip_date != date:
            y = trip_date.year
            m = trip_date.month
            d = trip_date.day
            y2 = trip_date2.year
            m2 = trip_date2.month
            d2 = trip_date2.day
    #
    affairs = Affairs.objects.select_related().filter(date_in__lte=date4, date_out__gte=date3)
    #
    affairs2 = Affairs.objects.select_related().filter(date_in__lte=date4, date_out=None)
    #
    affairs3 = Affairs.objects.select_related().filter(date_in__range=(date3, date4))
    #
    all_deals = Affairs.objects.count()
    # сколько заплатили
    all_deals_already = \
        Affairs.objects. \
            filter(date_in__lte=date4, date_out__lte=date4) \
            .aggregate(Sum('prisealready'))['prisealready__sum']
    # Общая сумма долга
    all_deals_prise = \
        Affairs.objects. \
            filter(date_in__lte=date4, date_out__lte=date4). \
            aggregate(Sum('prise'))['prise__sum']
    # Общая сумма вознаграждения
    all_deals_priseperformer = \
        Affairs.objects. \
            filter(deal_status='ON', date_in__lte=date4, date_out__lte=date4). \
            aggregate(Sum('priseperformer'))['priseperformer__sum']  # Общая сумма долга
    # Сумма выигранных дел
    win_deal = \
        Affairs.objects. \
            filter(deal_status='WI', date_in__lte=date4, date_out__gte=date3). \
            aggregate(Sum('prise'))['prise__sum']
    # Сколько дел выиграно
    win_deal1 = \
        Affairs.objects. \
            filter(deal_status='WI', date_in__lte=date4, date_out__gte=date3).count()
    # Сумма проигранных дел
    lose_deal = \
        Affairs.objects. \
            filter(deal_status='LO', date_in__lte=date4, date_out__gte=date3). \
            aggregate(Sum('prise'))['prise__sum']
    # Сколько дел проиграно
    lose_deal1 = Affairs.objects.filter(deal_status='LO', date_in__lte=date4, date_out__gte=date3).count()
    # Сколько дел в работе
    work_deal = Affairs.objects.filter(deal_status='ON', date_in__lte=date4, date_out__lte=date3).count()

    # Общая сумма долга
    all_deals_prise1 = \
        Affairs.objects. \
            filter(date_in__lte=date4, date_out=None). \
            aggregate(Sum('prise'))['prise__sum']
    # сколько заплатили
    all_deals_already1 = \
        Affairs.objects. \
            filter(date_in__lte=date4, date_out=None). \
            aggregate(Sum('prisealready'))['prisealready__sum']
    # Общая сумма долга
    all_deals_priseperformer1 = \
        Affairs.objects. \
            filter(date_in__lte=date4, date_out=None). \
            aggregate(Sum('priseperformer'))['priseperformer__sum']
    work_deal1 = Affairs.objects. \
        filter(deal_status='ON', date_in__lte=date4, date_out=None).count()

    test = Affairs.objects.filter(deal_status='ON')
    list2 = list()
    for staff in test:
        qs1 = staff.performer.all()
        qs2 = qs1.values('id')
        a = list(qs2)
        i = 0
        len1 = len(a)
        while i < len1:
            b = a[i]
            c = b['id']
            list2.append(c)
            i += 1
    list3 = set(list2)
    performer_work = Performers.objects.filter(id__in=list3).count()
    performer_all = Performers.objects.count()
    if all_deals_already is None:
        all_deals_already = 0
    if all_deals_prise is None:
        all_deals_prise = 0
    if all_deals_priseperformer is None:
        all_deals_priseperformer = 0
    if win_deal is None:
        win_deal = 0
    if win_deal1 is None:
        win_deal1 = 0
    if lose_deal is None:
        lose_deal = 0
    if lose_deal1 is None:
        lose_deal1 = 0
    if work_deal is None:
        work_deal = 0
    if all_deals_already1 is None:
        all_deals_already1 = 0
    if all_deals_prise1 is None:
        all_deals_prise1 = 0
    if all_deals_priseperformer1 is None:
        all_deals_priseperformer1 = 0
    if work_deal1 is None:
        work_deal1 = 0

    context = {
        'titlepage': 'Отчет по исполнителям от ' + str(date3) + ' до ' + str(date4),
        'for_table': affairs,
        'for_table2': affairs2,
        'for_table3': affairs3,
        'sum_all_rec': all_deals,
        'sum_all_spe': (all_deals_prise - all_deals_already) + (all_deals_prise1 - all_deals_already1),
        'all_deals_profit_supposed': (all_deals_prise - all_deals_priseperformer) + (
                all_deals_prise1 - all_deals_priseperformer1),
        'all_deals_profit': (all_deals_already - all_deals_priseperformer) + (
                all_deals_already1 - all_deals_priseperformer1),
        'all_deals_shoud': (all_deals_prise - all_deals_already) + (all_deals_prise1 - all_deals_already1),
        'all_deals_already': all_deals_already + all_deals_already1,
        'win_deal': win_deal,
        'lose_deal': lose_deal,
        'win_deal1': win_deal1,
        'lose_deal1': lose_deal1,
        'work_deal': work_deal + work_deal1,
        'performer_work': performer_work,
        'performer_dont_work': performer_all - performer_work,
        'y': y,
        'm': m,
        'd': d,
        'y2': y2,
        'm2': m2,
        'd2': d2,
    }
    if request.method == "POST" and 'del_rec' in request.POST:
        uid = request.POST['id']
        # receipt_del(uid)
        return render(request, 'finansy/dealreports.html', context)
    if request.method == "POST" and 'del_spe' in request.POST:
        uid = request.POST['id']
        # spending_del(uid)
        return render(request, 'finansy/dealreports.html', context)

    return render(request, 'finansy/dealreports.html', context)


# Список всего прихода
@permission_required('finansy.add_invoicespaids', raise_exception=True)
def finansy_today_all(request):
    date = timezone.datetime.now()
    y = date.year
    m = date.month
    d = date.day
    return redirect('finansy_today_date', y=y, m=m, d=d)


# Список всего прихода
@permission_required('finansy.settings', raise_exception=True)
def settings(request):
    return redirect('settings/in.html')



