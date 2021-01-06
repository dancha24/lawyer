# Generated by Django 3.1 on 2020-12-20 06:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('performers', '0003_auto_20200922_1754'),
        ('affairs', '0009_auto_20201219_1828'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExtraPerformer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sum', models.PositiveIntegerField(default=0, verbose_name='Сумма')),
                ('affairs', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='affairs.affairs', verbose_name='Дело')),
                ('performer', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='performers.performers', verbose_name='Исполнитель')),
            ],
            options={
                'verbose_name': 'Промежуток',
                'verbose_name_plural': 'Промежуток',
            },
        ),
    ]