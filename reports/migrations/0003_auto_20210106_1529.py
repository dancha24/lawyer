# Generated by Django 3.1 on 2021-01-06 08:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0002_dealrep'),
    ]

    operations = [
        migrations.DeleteModel(
            name='DealRep',
        ),
        migrations.AlterModelOptions(
            name='finsnsyrep',
            options={'verbose_name': 'Отчет', 'verbose_name_plural': 'Отчеты'},
        ),
    ]
