# Generated by Django 3.1 on 2021-01-06 08:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DealRep',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.FloatField(verbose_name='Название')),
            ],
            options={
                'verbose_name': 'Отчет по делу',
                'verbose_name_plural': 'Отчеты по делам',
            },
        ),
    ]
