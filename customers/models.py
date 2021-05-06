from django.db import models
from django.db.models import Sum


class WhereInfo(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Источник информации'
        verbose_name_plural = 'Источники информации'


class Customers(models.Model):
    URFACE = 'UR'
    FIZFACE = 'FI'
    FACE = (
        (URFACE, 'Юридическое лицо'),
        (FIZFACE, 'Физическое лицо'),
    )
    type = models.CharField(max_length=2, choices=FACE, default=FIZFACE, verbose_name='Тип')
    name = models.CharField(max_length=200, verbose_name='Имя')
    surname = models.CharField(max_length=200, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=200, verbose_name='Отчество')
    dr = models.DateField(verbose_name='День рождения', blank=True, null=True)
    pasno = models.CharField(max_length=200, verbose_name='Серия и номер паспорта', blank=True, null=True)
    pasby = models.CharField(max_length=200, verbose_name='Кем выдан', blank=True, null=True)
    pasdate = models.DateField(verbose_name='Дата выдачи паспорта', blank=True, null=True)
    paskod = models.CharField(max_length=200, verbose_name='Код подразделения паспорта', blank=True, null=True)
    address = models.CharField(max_length=200, verbose_name='Прописан', blank=True, null=True)
    tel = models.CharField(max_length=200, verbose_name='Телефон')
    whereknow = models.ForeignKey(WhereInfo, on_delete=models.SET_NULL, null=True, verbose_name='Источник информации')

    # Всего сделок
    def all_deals(self):
        from affairs.models import Affairs
        return Affairs.objects.filter(customers=self.id)

    all_deals.short_description = 'Все сделки'

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
        if self.all_deals().exists():
            return self.all_deals().aggregate(Sum('prisealready'))['prisealready__sum']
        else:
            return 0

    all_sum_already.short_description = 'Всего оплачено'

    # Общий долг
    def all_debt(self):
        debt = 0
        if self.all_deals().exists():
            for mat in self.all_deals():
                debt += mat.customers_debt()
            return debt
        else:
            return debt

    all_debt.short_description = 'Общий долг'

    # ФИО
    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic

    class Meta:
        verbose_name = 'Клиент'
        verbose_name_plural = 'Клиенты'
