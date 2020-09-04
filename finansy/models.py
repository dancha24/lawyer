from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.utils import timezone
from affairs.models import Affairs
from django.contrib.auth.models import User

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
