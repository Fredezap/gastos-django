# Generated by Django 4.2 on 2023-07-24 23:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_gastos', '0022_alter_movements_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movements',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 24, 23, 42, 49, 800418, tzinfo=datetime.timezone.utc)),
        ),
    ]
