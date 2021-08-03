from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from performers.models import Performers, JobCategories
from customers.models import Customers
from django.utils import timezone
from django.db.models import Sum

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
    deal_status = models.CharField(max_length=2, choices=STATUS_DEAL, default=ON, verbose_name='Статус Дела')
    prise_status = models.CharField(max_length=2, choices=STATUS_PRISE, default=NO, verbose_name='Статус Оплаты')
    com = models.TextField(blank=True, null=True, verbose_name='Комментарий по делу')
    manager = models.ForeignKey(Performers, verbose_name='Ведет дело', on_delete=models.PROTECT)
    manager_proc = models.FloatField(verbose_name='Процент ведущего', default=5)

    # Все приходы по делу
    def all_rec(self):
        from finansy.models import Receipt
        return Receipt.objects.filter(deal_id=self.id)

    # Все расходы по делу
    def all_spe(self):
        from finansy.models import Spending
        return Spending.objects.filter(deal_id=self.id)

    # Сумма всех возвратов по делу
    def all_spe_vozvrat(self):
        return self.all_rec().filter(category__name='Возврат клиенту').aggregate(Sum('sum'))['sum__sum']

    # Сумма приходов по делу
    def all_rec_sum(self):
        if not self.all_rec():
            return 0
        else:
            return self.all_rec().aggregate(Sum('sum'))['sum__sum']

    # Сумма расходов по делу
    def all_spe_sum(self):
        if not self.all_spe():
            return 0
        else:
            return self.all_spe().aggregate(Sum('sum'))['sum__sum']

    # Оперативный баланс по договору
    def profit_now(self):
        return self.all_rec_sum() - self.all_spe_sum()

    # Итоговый баланс по договору
    def profit_all(self):
        if self.manager_is_performer() == 2:
            return self.prise - self.performer_sum_all() - self.manager_proc_money() - self.all_spe_vozvrat()
        else:
            return self.prise - self.performer_sum_all() - self.all_spe_vozvrat()


    # Поцент ведущего по делу в деньгах
    def manager_proc_money(self):
        if self.manager_is_performer() == 2:
            return 0
        else:
            return self.prise / 100 * self.manager_proc

    # Является ли ведущий исполнителем
    def manager_is_performer(self):
        if self.manager.id in self.affair_performers_ids():
            if self.manager.all_sum_dop_id(af_id=self.id) == ExtraPerfomer.objects.get(affairs_id=self.id, performer_id=self.manager.id).sum:
                return 1  # Являеться сполнителем в допниках
            else:
                return 2  # Являеться исполнителем
        else:
            return 0  # Не Являеться исполнителем

    # Сколько оплатили ведущему
    def manager_proc_money_already(self):
        from finansy.models import Spending
        spe = Spending.objects.filter(deal_id=self.id, category__name='Оплата ведущему дело')
        if spe:
            return spe.aggregate(Sum('sum'))['sum__sum']
        else:
            return 0

    # Сколько осталось оплатить ведущему
    def manager_proc_money_debt(self):
        if self.manager_is_performer() == 2:
            return 0
        else:
            return self.manager_proc_money() - self.manager_proc_money_already()

    # Дела в работе
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
        return self.prise - float(self.all_rec_sum())

    # Задолжности клиентов по всем делам
    @staticmethod
    def customers_debt_all():
        summ = 0
        for af in Affairs.objects.all():
            summ += af.customers_debt()
        return summ

    # Айдишники допников дела
    def affair_extraaffairs_ids(self):
        return ExtraAffairs.objects.filter(affairs_id=self.id).values_list('id', flat=True)  # Айдишники исполнителей дела

    # Айдишники исполнителей дела
    def affair_performers_ids(self):
        return self.performer.all().values_list('id', flat=True)  # Айдишники исполнителей дела

    # Промежутки исполнителей по делу
    def affair_performers(self):
        return ExtraPerfomer.objects.filter(affairs_id=self.id, performer_id__in=self.affair_performers_ids())

    # Вознаграждения исполнителям по делу
    def performer_sum_all(self):
        if not not self.affair_performers():
            return self.affair_performers().aggregate(Sum('sum'))['sum__sum'] + self.manager_proc_money()
        else:
            return 0 + self.manager_proc_money()

    # Оплечено исполнителям по делу
    def performer_payment_all(self):
        if not not self.affair_performers():
            return self.affair_performers().aggregate(Sum('payment'))['payment__sum'] + self.manager_proc_money_already()
        else:
            return 0 + self.manager_proc_money_already()

    # Должны исполнителям по делу
    def performer_debt_all(self):
        return self.performer_sum_all() - self.performer_payment_all()

    # Сумма цен на все дела
    @staticmethod
    def prise_all():
        return Affairs.objects.all().aggregate(Sum('prise'))['prise__sum']

    # Приходы по всем делам
    @staticmethod
    def rec_all_affair():
        from finansy.models import Receipt
        return Receipt.objects.exclude(deal_id=None)

    # Сумма приходов по всем делам
    @staticmethod
    def rec_all_affair_sum():
        return Affairs.rec_all_affair().aggregate(Sum('sum'))['sum__sum']

    # # Сумма всех дел
    # @staticmethod
    # def prise_all():
    #     return Affairs.objects.all().aggregate(Sum('sum'))['sum__sum']

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дело'
        verbose_name_plural = 'Дела'


@receiver(post_save, sender=Affairs)
def add_exper(instance, **kwargs):
    for per in instance.performer.all():
        ExtraPerfomer.objects.get_or_create(affairs_id=instance.id, performer_id=per.id)
    ExtraPerfomer.objects.exclude(performer_id__in=instance.performer.all().values_list('id', flat=True)).filter(
        affairs_id=instance.id).delete()


class ExtraAffairs(models.Model):
    name = models.CharField(max_length=200, verbose_name='Номер дополнительного договора')
    affairs = models.ForeignKey(Affairs, default=None, on_delete=models.DO_NOTHING, verbose_name='Номер дела',
                                blank=True, null=True)
    sum = models.PositiveIntegerField(verbose_name="Сумма", default=0)
    comment = models.TextField(verbose_name="Коментарий", max_length=5000)
    file = models.FileField(verbose_name="Файл", blank=True, null=True)
    deal = models.CharField(max_length=200, verbose_name='Ссылка на сделку Битрикс')
    performer = models.ManyToManyField(Performers, default=None, verbose_name='Исполнитель', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Дополнительное дело'
        verbose_name_plural = 'Дополнительные дела'

    # Промежутки исполнителей по доп. делу
    def ex_affair_performers(self):
        performers_id = self.performer.all().values_list('id', flat=True)  # Айдишники исполнителей дела
        return ExtraPerfomer.objects.filter(extraaffairs_id=self.id, performer_id__in=performers_id)

    # Сумма вознаграждений по допнику
    def ex_affair_performers_sum(self):
        return self.ex_affair_performers().aggregate(Sum('sum'))['sum__sum']

    # Айдишники исполнителей допника
    def ex_affair_performers_ids(self):
        if self.performer:
            return self.performer.all().values_list('id', flat=True)  # Айдишники исполнителей допника
        else:
            return []

    # Айдишники исполнителей допника
    def ex_prise_already(self):
        from finansy.models import Receipt
        if Receipt.objects.filter(extra_deal_id=self.id).exists():
            return Receipt.objects.filter(extra_deal_id=self.id).aggregate(Sum('sum'))['sum__sum']
        else:
            return 0


@receiver(post_save, sender=ExtraAffairs)
def edit_balanse_add_rec(instance, created, **kwargs):
    for per in instance.performer.all():
        ExtraPerfomer.objects.get_or_create(extraaffairs_id=instance.id, performer_id=per.id)
        if per.id not in instance.affairs.affair_performers_ids():
            ExtraPerfomer.objects.create(affairs_id=instance.affairs.id, performer_id=per.id)
            Affairs.objects.get(pk=instance.affairs.id).performer.add(Performers.objects.get(pk=per.id))
        if created:
            ExtraPerfomer.objects.get_or_create(extraaffairs_id=instance.id, performer_id=per.id)
            if per.id not in instance.affairs.affair_performers_ids():
                ExtraPerfomer.objects.create(affairs_id=instance.affairs.id, performer_id=per.id)
                Affairs.objects.get(pk=instance.affairs.id).performer.add(Performers.objects.get(pk=per.id))
    ExtraPerfomer.objects.exclude(performer_id__in=instance.performer.all().values_list('id', flat=True)).filter(extraaffairs_id=instance.id).delete()
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
    extraaffairs = models.ForeignKey(ExtraAffairs, default=None, on_delete=models.CASCADE,
                                     verbose_name='Номер доп.дела',
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


@receiver(post_delete, sender=ExtraPerfomer)
def edit_balanse_del_rec(instance, **kwargs):
    if instance.extraaffairs is not None:
        af = Affairs.objects.get(extraaffairs=instance.extraaffairs)
        if instance.performer.id in af.affair_performers_ids():
            extra_af = ExtraPerfomer.objects.get(affairs_id=af.id, performer_id=instance.performer)
            extra_af.sum -= instance.sum
            extra_af.save()
