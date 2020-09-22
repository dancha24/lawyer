from django.db import models
from django.db.models import Sum


class JobCategories(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Категория работы'
        verbose_name_plural = 'Категории работы'


class Performers(models.Model):
    name = models.CharField(max_length=200, verbose_name='Имя')
    surname = models.CharField(max_length=200, verbose_name='Фамилия')
    patronymic = models.CharField(max_length=200, verbose_name='Отчество')
    whereknow = models.ManyToManyField(JobCategories, verbose_name='Категории работы')
    file = models.FileField(upload_to='performers/', verbose_name='Резюме', blank=True, null=True)

    # Всего сделок
    def all_deals(self):
        from affairs.models import Affairs
        return Affairs.objects.filter(performer=self.id)

    all_deals.short_description = 'Все сделки'

    # Фамилия И.О.
    def fio_min(self):
        return self.surname + ' ' + self.name[0] + '.' + self.patronymic[0] + '.'

    fio_min.short_description = 'ФИО'

    # Дел на сумму
    def all_sum(self):
        if self.all_deals().exists():
            return self.all_deals().aggregate(Sum('priseperformer'))['priseperformer__sum']
        else:
            return 0

    all_sum.short_description = 'Дел на сумму'

    # Всего оплачено
    def all_sum_already(self):
        if self.all_deals().exists():
            return self.all_deals().aggregate(Sum('priseperformeralready'))['priseperformeralready__sum']
        else:
            return 0

    all_sum_already.short_description = 'Всего оплачено'

    # Должны исполнителю
    def all_debt(self):
        debt = 0
        if self.all_deals().exists():
            for mat in self.all_deals():
                debt += mat.performer_debt()
            return debt
        else:
            return debt

    all_debt.short_description = 'Должны исполнителю'

    # ФИО
    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'


class PerformersDoc(models.Model):
    name = models.CharField(max_length=200, verbose_name='Номер договора')
    performer = models.ForeignKey(Performers, on_delete=models.DO_NOTHING, verbose_name='Исполнитель')

    def __str__(self):
        return self.name + ' ' + self.performer.fio_min()

    class Meta:
        verbose_name = 'Договор с исполнителями'
        verbose_name_plural = 'Договора с исполнителем'
