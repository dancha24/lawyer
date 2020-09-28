from django.db import models

# Create your models here.
class FinsnsyRep(models.Model):
    name = models.FloatField(verbose_name='Название')

    def __str__(self):
        return str(self.name)

    class Meta:
        verbose_name = 'Приход/расход'
        verbose_name_plural = 'Приход/расход'