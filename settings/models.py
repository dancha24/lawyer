from django.db import models

# Create your models here.


class Settings(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название')
    value = models.TextField(verbose_name='значение', default='Не установленно', blank=True, null=True)

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Настройка'
        verbose_name_plural = 'Настройки'
