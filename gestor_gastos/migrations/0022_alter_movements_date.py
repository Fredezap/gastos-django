# Generated by Django 4.2 on 2023-07-15 21:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_gastos', '0021_alter_category_current_funds_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movements',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2023, 7, 15, 21, 37, 22, 414695, tzinfo=datetime.timezone.utc)),
        ),
    ]
