from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from performers.models import Performers, JobCategories
from customers.models import Customers
from django.utils import timezone

ON = 'ON'
WIN = 'WI'
LOSE = 'LO'
STATUS_DEAL = (
    (ON, 'В процессе'),
    (WIN, 'Заверешено (Удачно)'),
    (LOSE, 'Заверешено (Неудачно)'),
)

NO = 'NO'
YES = 'YE'
STATUS_PRISE = (
    (NO, 'Не оплаченно'),
    (YES, 'Оплаченно'),
)


class Affairs(models.Model):
    name = models.CharField(max_length=200, verbose_name='Номер договора')
    deal = models.CharField(max_length=200, verbose_name='Ссылка на сделку Битрикс')
    date_in = models.DateField(default=timezone.now, verbose_name='Дата начала сделки')
    date_out = models.DateField(verbose_name='Дата окончания сделки', blank=True, null=True)
    customers = models.ForeignKey(Customers, default=None, on_delete=models.DO_NOTHING, verbose_name='Клиент')
    performer = models.ManyToManyField(Performers, default=None, verbose_name='Исполнитель',
                                       blank=True, null=True, related_name='perf')
    jobcategories = models.ForeignKey(JobCategories, default=None, on_delete=models.DO_NOTHING,
                                      verbose_name='Категория дела')
    prise = models.FloatField(verbose_name='Цена')
    priseperformer = models.FloatField(default=0, verbose_name='Вознаграждение для исполнителя', blank=True, null=True)
    prisealready = models.FloatField(default=0, verbose_name='Оплачено клиентом')
    priseperformeralready = models.FloatField(default=0, verbose_name='Выплачено исполнителю')
    deal_status = models.CharField(max_length=2, choices=STATUS_DEAL, default=ON, verbose_name='Статус Дела')
    prise_status = models.CharField(max_length=2, choices=STATUS_PRISE, default=NO, verbose_name='Статус Оплаты')

    # Дел в работе
    @staticmethod
    def deals_in():
        return Affairs.objects.filter(deal_status=ON)

    # Дел в работе кол-во
    @staticmethod
    def deals_in_count():
        return Affairs.deals_in().count()

    # Дел в работе на сумму
    @staticmethod
    def deals_in_prise_sum():
        summ = 0
        deals = Affairs.deals_in()
        for deal in deals:
            summ += deal.prise
        return summ

    # Дела в работе не оплаченные
    @staticmethod
    def deals_in_no_prise():
        return Affairs.deals_in().filter(prise_status=NO)

    # Кол-во дел в работе не оплаченных
    @staticmethod
    def deals_in_no_prise_count():
        return Affairs.deals_in_no_prise().count()

    # Дел в работе не оплаченных на сумму
    @staticmethod
    def deals_in_no_prise_sum():
        summ = 0
        deals = Affairs.deals_in_no_prise()
        for deal in deals:
            summ += deal.customers_debt()
        return summ

    # Клиент Должен
    def customers_debt(self):
        return self.prise - self.prisealready

    # Должны исполнителю
    def performer_debt(self):
        return self.priseperformer - self.priseperformeralready

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дело'
        verbose_name_plural = 'Дела'


@receiver(post_save, sender=Affairs)
def add_rec(instance, created, **kwargs):
    if created:
        for per in Performers.objects.all():
            prom = ExtraPerfomer()
            prom.affairs_id = instance.id
            prom.performer_id = per.id
            prom.sum = 0
            prom.save()


class ExtraAffairs(models.Model):
    name = models.CharField(max_length=200, verbose_name='Номер дополнительного договора')
    affairs = models.ForeignKey(Affairs, default=None, on_delete=models.DO_NOTHING, verbose_name='Номер дела',
                                blank=True, null=True)
    sum = models.PositiveIntegerField(verbose_name="Сумма", default=0)
    comment = models.TextField(verbose_name="Коментарий", max_length=5000)
    file = models.FileField(verbose_name="Файл", blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дополнительное дело'
        verbose_name_plural = 'Дополнительные дела'


@receiver(post_save, sender=ExtraAffairs)
def edit_balanse_add_rec(instance, created, **kwargs):
    if created:
        balance_now = Affairs.objects.get(id=instance.affairs_id)
        balance_now.prise += instance.sum
        balance_now.save()


@receiver(post_delete, sender=ExtraAffairs)
def edit_balanse_del_rec(instance, **kwargs):
    balance_now = Affairs.objects.get(id=instance.affairs_id)
    balance_now.prise -= instance.sum
    balance_now.save()


class ExtraPerfomer(models.Model):
    affairs = models.ForeignKey(Affairs, default=None, on_delete=models.CASCADE, verbose_name='Номер дела',
                                blank=True, null=True)
    performer = models.ForeignKey(Performers, default=None, on_delete=models.CASCADE, verbose_name='Исполнитель',
                                  blank=True, null=True)
    sum = models.PositiveIntegerField(verbose_name="Вознаграждение", default=0)
    payment = models.PositiveIntegerField(verbose_name="Оплачено", default=0)

    def __str__(self):
        return f'{self.sum}'

    class Meta:
        verbose_name = 'Промежуток'
        verbose_name_plural = 'Промежуток'
