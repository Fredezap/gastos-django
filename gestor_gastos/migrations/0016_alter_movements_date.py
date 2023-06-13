from django.db import migrations, models
from datetime import datetime
from django.utils.dateparse import parse_datetime

def actualizar_fecha_hora(apps, schema_editor):
    TuModelo = apps.get_model('gestor_gastos', 'Movements')

    for obj in TuModelo.objects.all():
        fecha_hora_str = obj.date.strftime("%Y-%m-%d %H:%M:%S")  # Formato actual
        fecha_hora_dt = parse_datetime(fecha_hora_str)  # Convertir a objeto datetime

        obj.date = fecha_hora_dt  # Asignar el objeto datetime sin formato

        # No es necesario guardar el objeto aquí, se guardará automáticamente al final de la migración

class Migration(migrations.Migration):

    dependencies = [
        ('gestor_gastos', '0015_remove_movements_date_time_movements_date'),
    ]

    operations = [
        migrations.RunPython(actualizar_fecha_hora),
        migrations.AlterField(
            model_name='movements',
            name='date',
            field=models.DateTimeField(default=datetime.now),
        ),
    ]