from django.shortcuts import render
from django.contrib.auth.decorators import login_required, permission_required
from affairs.models import Affairs, ExtraPerfomer, ExtraAffairs
from finansy.models import Receipt
from django.db.models import Sum
from performers.models import Performers
from datetime import datetime, date
from django.shortcuts import redirect
from .forms import FormForReportGlavLaw


# Все отчеты
@permission_required('reports.view_reports', raise_exception=True)  # Проверка прав
def reports_all(request):
    context = {
        'menu': 'reports',
        'submenu': 'reports_all',
        'titlepage': 'Отчеты',
    }

    return render(request, 'reports/reports_all.html', context)


# Список всех дел по фильтру
@permission_required('reports.view_affairs', raise_exception=True)  # Проверка прав
def report_glav_law(request):
    if request.method == "POST":
        form = FormForReportGlavLaw(request.POST)
        if form.is_valid():
            return redirect('report_glav_law_ans', date_in=form.cleaned_data['date_in'],
                            date_in_max=form.cleaned_data['date_in_max'],
                            performer_id=form.cleaned_data['performer_id'].id)
    else:
        form = FormForReportGlavLaw()
    context = {
        'form': form,
        'menu': 'reports',
        'submenu': 'affairs_all',
        'titlepage': 'Отчет по главному юристу',
    }

    return render(request, 'reports/report_glav_law.html', context)


# Отчет по главному юристу старый
@permission_required('reports.view_affairs', raise_exception=True)  # Проверка прав
def report_glav_law_ans_old(request, date_in, date_in_max, performer_id):
    performer = Performers.objects.get(pk=performer_id)

    affairs_all = Affairs.objects.all().filter(date_in__gte=date_in, date_in__lte=date_in_max)
    affairs_per = affairs_all.filter(performer=performer.id)
    affairs = affairs_all.exclude(performer=performer.id)

    extra_per_all = ExtraPerfomer.objects.filter(affairs_id__in=affairs_per.all().values_list('id', flat=True))
    sum_nagrada = 0
    sum_pay = 0
    sum_debt = 0

    if affairs_per:
        sum_nagrada = extra_per_all.aggregate(Sum('sum'))['sum__sum']
        sum_pay = extra_per_all.aggregate(Sum('payment'))['payment__sum']
        sum_debt = sum_nagrada - sum_pay

    sum_dela_ved = 0
    if affairs:
        sum_dela_ved = affairs.aggregate(Sum('prise'))['prise__sum']

    for af in affairs_per:
        ex = ExtraAffairs.objects.filter(affairs_id=af.id)
        for e in ex:
            if ExtraPerfomer.objects.get(performer=8, affairs_id=af.id) == ExtraPerfomer.objects.get(performer=8,
                                                                                                     extraaffairs_id=e.id):
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
        'menu': 'reports',
        'submenu': 'affairs_all',
        'titlepage': 'Отчет по главному юристу ' + performer.fio_min(),
    }

    return render(request, 'reports/report_glav_law_ans_old.html', context)


# Отчет по главному юристу
@permission_required('reports.view_affairs', raise_exception=True)  # Проверка прав
def report_glav_law_ans(request, date_in, date_in_max, performer_id):
    sum_debt = 0  #
    sum_dela_ved = 0  # Сумма приходов по делам и допникам которые ведет.
    sum_bonus_dela_ved = 0  # Вознаграждение по делам и допникам которые ведет.
    sum_bonus_dela_ved_already = 0  # Уже оплаченые Бонусы по ведению за дела, по которым был приход
    deals_ids = []  # Айдишники дел для подсчета оплаты бонуса

    performer = Performers.objects.get(pk=performer_id)

    all_rec = Receipt.objects.filter(date__gte=date_in, date__lte=date_in_max, deal__manager=performer)

    for rec in all_rec:
        if rec.category.name == 'Дополнительное соглашение':
            ids = performer.id
            idss = rec.extra_deal.ex_affair_performers_ids()
            if performer.id not in rec.extra_deal.ex_affair_performers_ids():
                sum_dela_ved += rec.sum
                sum_bonus_dela_ved += rec.sum / 100 * rec.deal.manager_proc
        else:
            if rec.deal.manager_is_performer() != 2:
                sum_dela_ved += rec.sum
                sum_bonus_dela_ved += rec.sum / 100 * rec.deal.manager_proc
        if rec.deal.id not in deals_ids:
            sum_bonus_dela_ved_already += rec.deal.manager_proc_money_already()
            deals_ids.append(rec.deal.id)

    context = {
        'performer': performer,

        'all_rec': all_rec,
        'sum_dela_ved': sum_dela_ved,
        'sum_bonus_dela_ved': sum_bonus_dela_ved,
        'sum_bonus_dela_ved_already': sum_bonus_dela_ved_already,
        'sum_bonus_dela_ved_debt': sum_bonus_dela_ved - sum_bonus_dela_ved_already,
        'menu': 'reports',
        'submenu': 'affairs_all',
        'titlepage': 'Отчет по главному юристу ' + performer.fio_min(),
    }

    return render(request, 'reports/report_glav_law_ans.html', context)
