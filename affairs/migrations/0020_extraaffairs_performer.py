# Generated by Django 3.1 on 2021-06-03 05:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('performers', '0004_auto_20210122_1341'),
        ('affairs', '0019_extraperfomer_extraaffairs'),
    ]

    operations = [
        migrations.AddField(
            model_name='extraaffairs',
            name='performer',
            field=models.ManyToManyField(blank=True, default=None, null=True, to='performers.Performers', verbose_name='Исполнитель'),
        ),
    ]
