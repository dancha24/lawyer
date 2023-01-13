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


class Konkurs(models.Model):
    message = models.TextField(verbose_name='Сообщение', blank=True, null=True)
    datain = models.TextField(verbose_name='Сообщение', blank=True, null=True)
    dataout = models.TextField(verbose_name='Сообщение', blank=True, null=True)

    def __str__(self):
        return self.message

    class Meta:
        verbose_name = 'Конкурс'
        verbose_name_plural = 'Конкурсы'


class PlayerKonkurs(models.Model):
    username = models.TextField(verbose_name='Сообщение', blank=True, null=True)
    konkurs = models.ForeignKey(Konkurs, default=None, on_delete=models.DO_NOTHING, verbose_name='Конкурс')
    win = models.BooleanField(default=True, verbose_name='Выиграл или нет')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Участник конкурса'
        verbose_name_plural = 'Участники конкурса'


class ChatsForKonkurs(models.Model):
    usernamechat = models.TextField(verbose_name='Паблик', blank=True, null=True)
    useruser = models.ForeignKey(Konkurs, default=None, on_delete=models.DO_NOTHING, verbose_name='Юзер')
    privyazka = models.BooleanField(default=True, verbose_name='Привязка')

    def __str__(self):
        return self.usernamechat

    class Meta:
        verbose_name = 'Паблик'
        verbose_name_plural = 'Паблики'
