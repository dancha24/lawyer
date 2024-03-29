# Generated by Django 3.1 on 2020-12-30 18:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performers', '0003_auto_20200922_1754'),
        ('affairs', '0012_auto_20201222_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraperfomer',
            name='payment',
            field=models.PositiveIntegerField(default=0, verbose_name='Оплачено'),
        ),
        migrations.AlterField(
            model_name='affairs',
            name='performer',
            field=models.ManyToManyField(blank=True, default=None, null=True, related_name='perf', to='performers.Performers', verbose_name='Исполнитель'),
        ),
        migrations.AlterField(
            model_name='extraaffairs',
            name='file',
            field=models.FileField(blank=True, upload_to='', verbose_name='Файл'),
        ),
        migrations.AlterField(
            model_name='extraperfomer',
            name='sum',
            field=models.PositiveIntegerField(default=0, verbose_name='Вознаграждение'),
        ),
    ]
