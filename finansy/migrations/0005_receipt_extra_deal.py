# Generated by Django 3.1 on 2021-07-06 11:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('affairs', '0023_affairs_manager_proc'),
        ('finansy', '0004_spending_performers'),
    ]

    operations = [
        migrations.AddField(
            model_name='receipt',
            name='extra_deal',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='affairs.extraaffairs', verbose_name='Допник'),
        ),
    ]