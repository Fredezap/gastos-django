# Generated by Django 4.2 on 2023-07-28 22:41

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_gastos', '0023_alter_movements_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movements',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 28, 22, 41, 58, 385151, tzinfo=datetime.timezone.utc)),
        ),
    ]