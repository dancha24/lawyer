# Generated by Django 3.1 on 2022-03-18 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('settings', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='settings',
            name='value',
            field=models.TextField(blank=True, null=True, verbose_name='значение'),
        ),
    ]
