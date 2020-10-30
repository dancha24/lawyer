from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from affairs.models import Affairs
from django.contrib.auth.models import User
from datetime import datetime

da = datetime.now()
CASH = 'CH'
CARD = 'CD'
BANK = 'BK'
MONEY = (
    (CASH, 'Наличные'),
    (CARD, 'Карта'),
    (BANK, 'Расчетный счет'),
)


class CategoriesOfReceipt(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория прихода'
        verbose_name_plural = 'Категории прихода'


class Receipt(models.Model):
    sum = models.FloatField(verbose_name='Сумма')
    com = models.TextField(verbose_name='Коментарий', blank=True, null=True)
    type = models.CharField(max_length=2, choices=MONEY, default=CASH, verbose_name='Вид движения средств')
    date = models.DateField(default=timezone.now, verbose_name='Дата прихода')
    category = models.ForeignKey(CategoriesOfReceipt, on_delete=models.DO_NOTHING, verbose_name='Категория')
    deal = models.ForeignKey(Affairs, on_delete=models.DO_NOTHING, verbose_name='Дело', blank=True, null=True)

    def __str__(self):
        return str(self.sum) + ' ' + str(self.category)

    class Meta:
        verbose_name = 'Запись прихода'
        verbose_name_plural = 'Записи прихода'

    # Дел в работе сегодня
    @staticmethod
    def receipt_in():
        return Receipt.objects.filter(date=datetime.now())

    # Дел в работе кол-во сегодня
    @staticmethod
    def receipt_in_count():
        return Receipt.receipt_in().count()

    # Дел в работе на сумму сегодня
    @staticmethod
    def receipt_in_prise_sum():
        summ = 0
        deals = Receipt.receipt_in()
        for deal in deals:
            summ += deal.sum
        return (summ)

    # Дел в работе месяц
    @staticmethod
    def receipt_in_mount():
        return Receipt.objects.filter(date__month=da.month)

    # Дел в работе месяц
    @staticmethod
    def receipt_in_count_mount():
        return Receipt.receipt_in_mount().count()

    # Дел в работе на сумму
    @staticmethod
    def receipt_in_prise_sum_mount():
        summ = 0
        deals = Receipt.receipt_in_mount()
        for deal in deals:
            summ += deal.sum
        return (summ)

    # Фильтр прихода.
    @staticmethod
    def receipt_in_filter(request):
        year = request.GET.get('date__year')
        month = request.GET.get('date__month')
        day = request.GET.get('date__day')
        deal = request.GET.get('deal__id__exact')
        type_exact = request.GET.get('type__exact')
        if year == None and month == None and day == None and deal == None and type_exact == None:
            found = Receipt.objects.filter()
        elif year == None and month == None and day == None and deal == None:
            found = Receipt.objects.filter(type=type_exact)
        elif month == None and day == None and deal == None and type_exact == None:
            found = Receipt.objects.filter(date__year=year)
        elif year == None and month == None and day == None and type_exact == None:
            found = Receipt.objects.filter(deal__id=deal)
        elif year == None and month == None and day == None:
            found = Receipt.objects.filter(deal__id=deal).filter(type=type_exact)
        elif day == None and type_exact == None and deal == None:
            found = Receipt.objects.filter(date__year=year).filter(date__month=month)
        elif month == None and day == None and type_exact == None:
            found = Receipt.objects.filter(date__year=year).filter(deal__id=deal)
        elif month == None and day == None and deal == None:
            found = Receipt.objects.filter(date__year=year).filter(type=type_exact)
        elif month == None and day == None:
            found = Receipt.objects.filter(date__year=year).filter(deal__id=deal).filter(type=type_exact)
        elif day == None and deal == None:
            found = Receipt.objects.filter(date__year=year).filter(date__month=month).filter(type=type_exact)
        elif day == None and type_exact == None:
            found = Receipt.objects.filter(date__year=year).filter(date__month=month).filter(deal__id=deal)
        elif deal == None and type_exact == None:
            found = Receipt.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day)
        elif deal == None:
            found = Receipt.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day).filter(
                type=type_exact)
        elif type_exact == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day).filter(
                deal__id=deal)
        elif day == None:
            found = Receipt.objects.filter(date__year=year).filter(date__month=month).filter(deal__id=deal).filter(
                type=type_exact)
        else:
            found = Receipt.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day). \
                filter(deal__id=deal).filter(type=type_exact)
        return found

    # Фильтр
    @staticmethod
    def filter(request):
        summ = 0
        deals = Receipt.receipt_in_filter(request)
        for deal in deals:
            summ += deal.sum
        return (summ)

    # Дел в работе все время
    @staticmethod
    def receipt_in_all_time():
        return Receipt.objects.filter()

    # Дел в работе кол-во все время
    @staticmethod
    def receipt_in_count_all_time():
        return Receipt.receipt_in_all_time().count()

    # Дел в работе на сумму все время
    @staticmethod
    def receipt_in_prise_sum_all_time():
        summ = 0
        deals = Receipt.receipt_in_all_time()
        for deal in deals:
            summ += deal.sum
        return (summ)


@receiver(post_save, sender=Receipt)
def edit_balanse_add_rec(instance, created, **kwargs):
    if created:
        balance_now = FinansyBalance.objects.get(type=instance.type)
        balance_now.sum += instance.sum
        balance_now.save()
        if instance.deal:
            deal = Affairs.objects.get(id=instance.deal.id)
            deal.prisealready += instance.sum
            deal.save()
            if deal.prisealready >= deal.prise:
                deal.prise_status = 'YE'
                deal.save()


@receiver(post_delete, sender=Receipt)
def edit_balanse_del_rec(instance, **kwargs):
    balance_now = FinansyBalance.objects.get(type=instance.type)
    balance_now.sum -= instance.sum
    balance_now.save()
    if instance.deal:
        deal = Affairs.objects.get(id=instance.deal.id)
        deal.prisealready -= instance.sum
        deal.save()
        if deal.prisealready < deal.prise:
            deal.prise_status = 'NO'
            deal.save()


class CategoriesOfSpending(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория расхода'
        verbose_name_plural = 'Категории расхода'


class Spending(models.Model):
    sum = models.FloatField(verbose_name='Сумма')
    com = models.TextField(verbose_name='Коментарий', blank=True, null=True)
    type = models.CharField(max_length=2, choices=MONEY, default=CASH, verbose_name='Вид движения средств')
    date = models.DateField(default=timezone.now, verbose_name='Дата расхода')
    category = models.ForeignKey(CategoriesOfSpending, on_delete=models.CASCADE, verbose_name='Категория')
    user_do = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Отвественный')
    deal = models.ForeignKey(Affairs, on_delete=models.DO_NOTHING, verbose_name='Дело', blank=True, null=True)

    def __str__(self):
        return str(self.sum) + ' ' + str(self.category)

    class Meta:
        verbose_name = 'Запись расхода'
        verbose_name_plural = 'Записи расхода'

    # Фильтр прихода.
    @staticmethod
    def spending_in_filter(request):
        year = request.GET.get('date__year')
        month = request.GET.get('date__month')
        day = request.GET.get('date__day')
        deal = request.GET.get('deal__id__exact')
        type_exact = request.GET.get('type__exact')
        category = request.GET.get('category__id__exact')
        if year == None and month == None and day == None and deal == None and type_exact == None and category == None:
            found = Spending.objects.filter()
        elif year == None and month == None and day == None and deal == None:
            found = Spending.objects.filter(type=type_exact)
        elif month == None and day == None and deal == None and type_exact == None:
            found = Spending.objects.filter(date__year=year)
        elif year == None and month == None and day == None and type_exact == None:
            found = Spending.objects.filter(deal__id=deal)
        elif year == None and month == None and day == None:
            found = Spending.objects.filter(deal__id=deal).filter(type=type_exact)
        elif day == None and type_exact == None and deal == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month)
        elif month == None and day == None and type_exact == None:
            found = Spending.objects.filter(date__year=year).filter(deal__id=deal)
        elif month == None and day == None and deal == None:
            found = Spending.objects.filter(date__year=year).filter(type=type_exact)
        elif month == None and day == None:
            found = Spending.objects.filter(date__year=year).filter(deal__id=deal).filter(type=type_exact)
        elif day == None and deal == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(type=type_exact)
        elif day == None and type_exact == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(deal__id=deal)
        elif day == None and category == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(deal__id=deal).filter(type=type_exact)
        elif deal == None and type_exact == None and category == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day)
        elif deal == None and type_exact == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day).filter(category__id=category)
        elif deal == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day).filter(
                type=type_exact)
        elif type_exact == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day).filter(deal__id=deal)
        elif day == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(deal__id=deal).filter(
                type=type_exact)
        elif year == None and month == None and day == None and deal == None and type_exact == None and category == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day).filter(deal__id=deal).filter(
                type=type_exact).filter(category_id=category)
        elif year == None and month == None and day == None and deal == None:
            found = Spending.objects.filter(type=type_exact).filter(category_id=category)
        elif year == None and month == None and day == None and deal == None and type_exact == None:
            found = Spending.objects.filter(category__id=category)
        elif category == None:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day).filter(deal__id=deal).filter(
                type=type_exact)
        else:
            found = Spending.objects.filter(date__year=year).filter(date__month=month).filter(date__day=day). \
                filter(deal__id=deal).filter(type=type_exact)
        return found

    # Фильтр
    @staticmethod
    def filter(request):
        summ = 0
        deals = Spending.spending_in_filter(request)
        for deal in deals:
            summ += deal.sum
        return (summ)
    # Дел в работе все время
    @staticmethod
    def spending_in_all_time():
        return Spending.objects.filter()

    # Дел в работе кол-во все время
    @staticmethod
    def spending_in_count_all_time():
        return Spending.spending_in_all_time().count()

    # Дел в работе на сумму все время
    @staticmethod
    def spending_in_prise_sum_all_time():
        summ = 0
        deals = Spending.spending_in_all_time()
        for deal in deals:
            summ += deal.sum
        return (summ)
    # Дел в работе сегодня
    @staticmethod
    def spending_in():
        return Spending.objects.filter(date=datetime.now())

    # Дел в работе кол-во сегодня
    @staticmethod
    def spending_in_count():
        return Spending.spending_in().count()

    # Дел в работе на сумму сегодня
    @staticmethod
    def spending_in_prise_sum():
        summ = 0
        deals = Spending.spending_in()
        for deal in deals:
            summ += deal.sum
        return (summ)

    # Дел в работе месяц
    @staticmethod
    def spending_in_mount():
        return Spending.objects.filter(date__month=da.month)

    # Дел в работе месяц
    @staticmethod
    def spending_in_count_mount():
        return Spending.spending_in_mount().count()

    # Дел в работе на сумму
    @staticmethod
    def spending_in_prise_sum_mount():
        summ = 0
        deals = Spending.spending_in_mount()
        for deal in deals:
            summ += deal.sum
        return (summ)

@receiver(post_save, sender=Spending)
def edit_balanse_add_spe(instance, created, **kwargs):
    if created:
        balance_now = FinansyBalance.objects.get(type=instance.type)
        balance_now.sum -= instance.sum
        balance_now.save()
        if instance.category.id == 1:
            deal = Affairs.objects.get(id=instance.deal.id)
            deal.priseperformeralready += instance.sum
            deal.save()


@receiver(post_delete, sender=Spending)
def edit_balanse_del_spe(instance, **kwargs):
    balance_now = FinansyBalance.objects.get(type=instance.type)
    balance_now.sum += instance.sum
    balance_now.save()
    if instance.category.id == 1:
        deal = Affairs.objects.get(id=instance.deal.id)
        deal.priseperformeralready -= instance.sum
        deal.save()


class FinansyBalance(models.Model):
    sum = models.FloatField(verbose_name='Баланс')
    type = models.CharField(max_length=2, choices=MONEY, default=CASH, verbose_name='Вид движения средств')

    def __str__(self):
        return str(self.type)

    class Meta:
        verbose_name = 'Баланс'
        verbose_name_plural = 'Балансы'
