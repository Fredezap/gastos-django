# Generated by Django 4.2 on 2023-05-31 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_gastos', '0005_category_is_payment'),
    ]

    operations = [
        migrations.AddField(
            model_name='movements',
            name='still_exist',
            field=models.BooleanField(default=True),
        ),
    ]
