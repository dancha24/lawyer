# Generated by Django 3.1 on 2022-03-18 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0002_auto_20220318_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='value',
            field=models.TextField(blank=True, default='Не установленно', null=True, verbose_name='значение'),
        ),
    ]
