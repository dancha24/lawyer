# Generated by Django 3.1 on 2021-06-06 19:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affairs', '0022_auto_20210607_0237'),
    ]

    operations = [
        migrations.AddField(
            model_name='affairs',
            name='manager_proc',
            field=models.FloatField(default=5, verbose_name='Процент ведущего'),
        ),
    ]