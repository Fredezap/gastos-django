# Generated by Django 4.2 on 2023-06-01 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_gastos', '0009_alter_category_current_funds_alter_category_detail_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='movements',
            name='is_savings_withdraw',
            field=models.BooleanField(default=False),
        ),
    ]
