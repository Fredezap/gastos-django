# Generated by Django 4.2 on 2023-06-03 03:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_gastos', '0013_remove_movements_date_time_movements_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movements',
            name='date',
        ),
        migrations.AddField(
            model_name='movements',
            name='date_time',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
