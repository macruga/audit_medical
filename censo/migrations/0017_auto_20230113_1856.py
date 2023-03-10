# Generated by Django 3.0.10 on 2023-01-13 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('censo', '0016_auto_20230110_1845'),
    ]

    operations = [
        migrations.AlterField(
            model_name='censomodel',
            name='origen_evento_id',
            field=models.ForeignKey(db_column='origen_evento_id', on_delete=django.db.models.deletion.PROTECT, related_name='censo_origen_evento', to='censo.OrigenEventoModel'),
        ),
        migrations.AlterField(
            model_name='censomodel',
            name='tipo_habitacion_id',
            field=models.ForeignKey(db_column='tipo_habitacion_id', on_delete=django.db.models.deletion.PROTECT, related_name='censo_tipo_habitacion', to='censo.TipoHabitacionModel'),
        ),
        migrations.AlterField(
            model_name='censomodel',
            name='tipo_ingreso_id',
            field=models.ForeignKey(db_column='tipo_ingreso_id', on_delete=django.db.models.deletion.PROTECT, related_name='censo_tipo_ingreso', to='censo.TipoIngresoModel'),
        ),
    ]
