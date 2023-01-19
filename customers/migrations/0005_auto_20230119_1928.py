# Generated by Django 3.1 on 2023-01-19 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customers', '0004_auto_20230118_1756'),
    ]

    operations = [
        migrations.CreateModel(
            name='SpravKaspiVarVipis',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Детали')),
                ('oper', models.CharField(max_length=200, verbose_name='Операция')),
            ],
            options={
                'verbose_name': 'Вариант для выписки',
                'verbose_name_plural': 'Варианты для выписки',
            },
        ),
        migrations.AlterField(
            model_name='customers',
            name='adresfiktiv',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Фиктивный адрес для договора аренды'),
        ),
        migrations.AlterField(
            model_name='customers',
            name='cityfiktiv',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Фиктивный город для справок'),
        ),
    ]
