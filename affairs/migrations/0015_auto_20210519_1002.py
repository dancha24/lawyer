# Generated by Django 3.1 on 2021-05-19 03:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('affairs', '0014_auto_20210106_1449'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='affairs',
            name='prisealready',
        ),
        migrations.AlterField(
            model_name='extraaffairs',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='', verbose_name='Файл'),
        ),
    ]