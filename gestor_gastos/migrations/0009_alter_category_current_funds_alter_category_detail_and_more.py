# Generated by Django 4.2 on 2023-06-01 05:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gestor_gastos', '0008_alter_movements_detail_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='current_funds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='category',
            name='detail',
            field=models.TextField(blank=True, max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='goal_founds',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='category',
            name='last_funds',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='category',
            name='percentage',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=10, null=True),
        ),
        migrations.AlterField(
            model_name='movements',
            name='amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
        migrations.AlterField(
            model_name='movements',
            name='detail',
            field=models.TextField(blank=True, default='-', max_length=350, null=True),
        ),
        migrations.AlterField(
            model_name='movements',
            name='salary_funds_after',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='movements',
            name='salary_funds_before',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='movements',
            name='savings',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='movements',
            name='savings_funds_after',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='movements',
            name='savings_funds_before',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AlterField(
            model_name='movements',
            name='total_amount',
            field=models.DecimalField(decimal_places=2, max_digits=10),
        ),
    ]
