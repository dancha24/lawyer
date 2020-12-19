from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from finansy import forms
from django.shortcuts import redirect
from finansy.models import *
from django.forms.models import modelform_factory
from django.shortcuts import get_object_or_404
from django.db.models import Sum
# from report.defs import report_receiptspending, report_owe_us, report_car_of_day
import datetime
from datetime import datetime
from django.shortcuts import render
from django.views.generic import DetailView, ListView, CreateView
from django.views.generic.edit import UpdateView, DeleteView


# Create your views here.
# Список всего прихода
# @permission_required('finansy.add_invoicespaids', raise_exception=True)
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
        #form = forms.DateForm(request.POST)
        if trip_date != date:
            #fa = form.cleaned_data['gaga']
            #date = datetime.datetime.strptime(fa, '%Y-%m-%d')
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


# Список всего прихода
@permission_required('finansy.add_invoicespaids', raise_exception=True)
def finansy_today_all(request):
    date = timezone.datetime.now()
    y = date.year
    m = date.month
    d = date.day

    return redirect('finansy_today_date', y=y, m=m, d=d)
