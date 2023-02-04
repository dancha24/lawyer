from django.db import models
from django.db.models import Sum
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete


class WhereInfo(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Источник информации'
        verbose_name_plural = 'Источники информации'


class SpravKaspiVarVipis(models.Model):
    name = models.CharField(max_length=200, verbose_name='Детали')
    oper = models.CharField(max_length=200, verbose_name='Операция')
    minprise = models.FloatField(verbose_name='Минимальная цена', blank=True, null=True)
    maxprise = models.FloatField(verbose_name='Максимальная цена', blank=True, null=True)
    krat = models.FloatField(verbose_name='Кратность', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вариант для выписки'
        verbose_name_plural = 'Варианты для выписки'


class TildaInSum(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    phone = models.CharField(max_length=200, verbose_name='Телефон')
    summa = models.FloatField(verbose_name='Сумма', blank=True, null=True)
    incrm = models.BooleanField(max_length=200, verbose_name='Есть ли в црм', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Оплата через тильду'
        verbose_name_plural = 'Оплаты через тильду'


class Customers(models.Model):
    URFACE = 'UR'
    FIZFACE = 'FI'
    FACE = (
        (URFACE, 'Юридическое лицо'),
        (FIZFACE, 'Физическое лицо'),
    )
    MAN = 'UR'
    WMAN = 'FI'
    POL = (
        (MAN, 'Мужской'),
        (WMAN, 'Женский'),
    )
    type = models.CharField(max_length=2, choices=FACE, default=FIZFACE, verbose_name='Тип')
    name = models.CharField(max_length=200, verbose_name='Имя')
    surname = models.CharField(max_length=200, verbose_name='Фамилия')
    pol = models.CharField(max_length=2, choices=POL, verbose_name='Пол')
    patronymic = models.CharField(max_length=200, verbose_name='Отчество', blank=True, null=True)
    dr = models.DateField(verbose_name='День рождения')
    paswhat = models.CharField(max_length=200, verbose_name='Удостоверение личности (прим: Паспорт РФ', default='Паспорт РФ')
    pasno = models.CharField(max_length=200, verbose_name='Серия и номер документа')
    pasby = models.CharField(max_length=200, verbose_name='Кем выдан')
    pasdate = models.DateField(verbose_name='Дата выдачи паспорта')
    paskod = models.CharField(max_length=200, verbose_name='Код подразделения паспорта', blank=True, null=True)
    address = models.CharField(max_length=200, verbose_name='Прописан', blank=True, null=True)
    tel = models.CharField(max_length=200, verbose_name='Телефон')
    whereknow = models.ForeignKey(WhereInfo, on_delete=models.SET_NULL, verbose_name='Источник информации', blank=True, null=True)
    # Для покера
    adresfiktiv = models.CharField(max_length=200, verbose_name='Фиктивный адрес для договоров и справок', blank=True, null=True)
    cityfiktiv = models.CharField(max_length=200, verbose_name='Фиктивный город для договоров и справок', blank=True, null=True)
    byuser = models.ForeignKey(User, default=1, verbose_name='Кто добавил в программу', on_delete=models.PROTECT)

    # Всего сделок
    def all_deals(self):
        from affairs.models import Affairs
        return Affairs.objects.filter(customers=self.id)

    all_deals.short_description = 'Все сделки'

    # Все приходы
    def all_rec(self):
        from affairs.models import Affairs
        from finansy.models import Receipt
        return Receipt.objects.filter(
            deal_id__in=Affairs.objects.filter(customers=self.id).values_list('id', flat=True))

    # Фамилия И.О.
    def fio_min(self):
        return self.surname + ' ' + self.name[0] + '.' + self.patronymic[0] + '.'

    fio_min.short_description = 'ФИО'

    # Дел на сумму
    def all_sum(self):
        if self.all_deals().exists():
            return self.all_deals().aggregate(Sum('prise'))['prise__sum']
        else:
            return 0

    all_sum.short_description = 'Дел на сумму'

    # Всего оплачено
    def all_sum_already(self):
        summ = 0
        if self.all_deals().exists():
            for deal in self.all_deals():
                summ += deal.all_rec_sum()
        return summ

    all_sum_already.short_description = 'Всего оплачено'

    # Общий долг
    def all_debt(self):
        summ = 0
        if self.all_deals().exists():
            for deal in self.all_deals():
                summ += deal.customers_debt()
        return summ

    all_debt.short_description = 'Общий долг'

    # ФИО
    def __str__(self):
        return self.surname + ' ' + self.name

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'


# @receiver(post_save, sender=Customers)
# def edit_balanse_add_rec(instance, created, **kwargs):
#     if created:
#         instance.byuser =
#         balance_now = FinansyBalance.objects.get(type=instance.type)
#         balance_now.sum += instance.sum
#         balance_now.save()
#         if instance.deal:
#             deal = Affairs.objects.get(id=instance.deal.id)
#             if deal.all_rec_sum() >= deal.prise:
#                 deal.prise_status = 'YE'
#                 deal.save()