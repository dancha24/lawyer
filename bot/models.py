from django.db import models
# Create your models here.


class Promocodes(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    sale = models.IntegerField(verbose_name='Скидка в рублях')
    linkpay = models.CharField(max_length=200,verbose_name='Ссылка на оплату')
    aktive = models.BooleanField(default=True, verbose_name='Активность')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Промокод'
        verbose_name_plural = 'Промокоды'


class Botset(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    set = models.TextField(verbose_name='Настройка', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
