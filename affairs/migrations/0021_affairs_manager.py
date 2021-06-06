# Generated by Django 3.1 on 2021-06-06 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performers', '0004_auto_20210122_1341'),
        ('affairs', '0020_extraaffairs_performer'),
    ]

    operations = [
        migrations.AddField(
            model_name='affairs',
            name='manager',
            field=models.ForeignKey(blank=True, default=8, null=True, on_delete=django.db.models.deletion.PROTECT, to='performers.performers', verbose_name='Ведет дело'),
        ),
    ]
