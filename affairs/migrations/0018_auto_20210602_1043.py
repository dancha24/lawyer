# Generated by Django 3.1 on 2021-06-02 03:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affairs', '0017_auto_20210602_1041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extraaffairs',
            name='deal',
            field=models.CharField(max_length=200, verbose_name='Ссылка на сделку Битрикс'),
        ),
    ]
