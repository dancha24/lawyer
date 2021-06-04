from django.db import models
from django.db.models import Sum
from django.utils import timezone
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from affairs import models as af_models


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
    email = models.CharField(max_length=200, verbose_name='Почта', blank=True, null=True)
    adres = models.CharField(max_length=200, verbose_name='Прописка', blank=True, null=True)
    birthday = models.DateField(max_length=200, verbose_name='Дата рождения', blank=True, null=True)
    pasno = models.CharField(max_length=200, verbose_name='Номер пасспорта', blank=True, null=True)
    pasby = models.CharField(max_length=200, verbose_name='Паспорт выдан', blank=True, null=True)
    pasdate = models.DateField(verbose_name='Дата выдачи паспорта', blank=True, null=True)
    paskod = models.CharField(max_length=200, verbose_name='Код подразделения паспорта', blank=True, null=True)
    tel = models.CharField(max_length=200, verbose_name='Телефон', blank=True, null=True)
    date_in = models.DateField(default=timezone.now, max_length=200, verbose_name='Дата принятия', blank=True, null=True)
    date_out = models.DateField(max_length=200, verbose_name='Дата увольнения', blank=True, null=True)

    # Всего сделок
    def all_deals(self):
        from affairs.models import Affairs
        return Affairs.objects.filter(performer=self.id)

    # Всего доп делов
    def all_ex_deals(self):
        from affairs.models import ExtraAffairs
        return ExtraAffairs.objects.filter(performer=self.id)

    all_deals.short_description = 'Все сделки'

    # Фамилия И.О.
    def fio_min(self):
        return self.surname + ' ' + self.name[0] + '.' + self.patronymic[0] + '.'

    fio_min.short_description = 'ФИО'

    # Дел на сумму
    def all_sum(self):
        summ = 0
        if self.all_deals().exists():
            from affairs.models import ExtraPerfomer
            for deal in self.all_deals():
                summ += ExtraPerfomer.objects.get(affairs_id=deal.id, performer_id=self.id).sum
        return summ

    all_sum.short_description = 'Дел на сумму'

    # Дел на сумму всех исполнителей
    @staticmethod
    def all_sum_all_performers():
        sum = 0
        for p in Performers.objects.all():
            sum += p.all_sum()
        return sum

    # Всего оплачено
    def all_sum_already(self):
        summ = 0
        if self.all_deals().exists():
            from affairs.models import ExtraPerfomer
            for deal in self.all_deals():
                summ += ExtraPerfomer.objects.get(affairs_id=deal.id, performer_id=self.id).payment
        return summ

    all_sum_already.short_description = 'Всего оплачено'

    # Всего оплачено всем исполнителям
    @staticmethod
    def all_sum_already_all_performers():
        sum = 0
        for p in Performers.objects.all():
            sum += p.all_sum_already()
        return sum

    # Всего должны всем исполнителям
    @staticmethod
    def all_debt_all_performers():
        sum = Performers.all_sum_all_performers() - Performers.all_sum_already_all_performers()
        return sum

    # Должны исполнителю
    def all_debt(self):
        return self.all_sum() - self.all_sum_already()

    all_debt.short_description = 'Должны исполнителю'

    # ФИО
    def __str__(self):
        return self.surname + ' ' + self.name + ' ' + self.patronymic

    class Meta:
        verbose_name = 'Исполнитель'
        verbose_name_plural = 'Исполнители'


# @receiver(post_save, sender=Performers)
# def add_rec(instance, created, **kwargs):
#     if created:
#         for per in af_models.Affairs.objects.all():
#             prom = af_models.ExtraPerfomer()
#             prom.affairs_id = per.id
#             prom.performer_id = instance.id
#             prom.sum = 0
#             prom.save()


class PerformersDoc(models.Model):
    name = models.CharField(max_length=200, verbose_name='Номер договора')
    performer = models.ForeignKey(Performers, on_delete=models.DO_NOTHING, verbose_name='Исполнитель')

    def __str__(self):
        return self.name + ' ' + self.performer.fio_min()

    class Meta:
        verbose_name = 'Договор с исполнителями'
        verbose_name_plural = 'Договора с исполнителем'
