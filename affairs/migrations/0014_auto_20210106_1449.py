# Generated by Django 3.1 on 2021-01-06 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performers', '0003_auto_20200922_1754'),
        ('affairs', '0013_auto_20201231_0136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='extraaffairs',
            name='name',
            field=models.CharField(max_length=200, verbose_name='Номер дополнительного договора'),
        ),
        migrations.AlterField(
            model_name='extraperfomer',
            name='affairs',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='affairs.affairs', verbose_name='Номер дела'),
        ),
        migrations.AlterField(
            model_name='extraperfomer',
            name='performer',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='performers.performers', verbose_name='Исполнитель'),
        ),
    ]
