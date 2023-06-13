# Generated by Django 4.2 on 2023-06-03 03:56

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_gastos', '0014_remove_movements_date_movements_date_time'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movements',
            name='date_time',
        ),
        migrations.AddField(
            model_name='movements',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
