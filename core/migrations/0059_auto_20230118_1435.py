# Generated by Django 3.0.10 on 2023-01-18 14:35

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0058_especialidadesmodel_serviciosmodel'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cumsmodel',
            name='atc_id',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='cantidad',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='cantidad_cum',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='concentracion',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='descripcion_comercial',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='estado_cum',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='estado_registro',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='fecha_activo',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='fecha_expedicion',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='fecha_inactivo',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='fecha_vencimiento',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='forma_farmaceutica',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='muestra_medica',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='owner',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='producto',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='registro_sanitario',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='titular',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='unidad',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='unidad_medida',
        ),
        migrations.RemoveField(
            model_name='cumsmodel',
            name='unidad_referencia',
        ),
        migrations.AddField(
            model_name='cumsmodel',
            name='antibiotico',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Si')], default=0, help_text='1: es antibiotico, 2. no es antibiotico'),
        ),
        migrations.AddField(
            model_name='cumsmodel',
            name='atc',
            field=models.CharField(default=1, help_text='Codigo ATC', max_length=100, validators=[core.validators.noSpacesStartEnd]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cumsmodel',
            name='codigo',
            field=models.CharField(default=1, help_text='Codigo cums del medicamento', max_length=200, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyDigitsAndDash]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='cumsmodel',
            name='descripcion',
            field=models.CharField(help_text='Descripcion comercial del medicamento', max_length=200, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersSpacesAndPunctuation]),
        ),
        migrations.AddField(
            model_name='cumsmodel',
            name='nombre_medicamento',
            field=models.CharField(default='Sin nombre', help_text='Nombre del medicamento administrado', max_length=2000, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersSpacesAndPunctuation]),
        ),
        migrations.AddField(
            model_name='cumsmodel',
            name='registro_invima',
            field=models.CharField(help_text='Registro Sanitario INVIMA', max_length=200, null=True, validators=[core.validators.noSpacesStartEnd]),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='descripcion_atc',
            field=models.CharField(blank=True, help_text='Descripcion Codigo ATC', max_length=200, null=True, validators=[core.validators.noSpacesStartEnd]),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='expediente_cum',
            field=models.CharField(help_text='Expediente Cum', max_length=200, validators=[core.validators.noSpacesStartEnd, core.validators.onlyDigits]),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='principio_activo',
            field=models.CharField(help_text='Principio activo del medicamento', max_length=200, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndDigits]),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='via_administracion',
            field=models.CharField(blank=True, help_text='Via de administracion del medicamento', max_length=100, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndDigits]),
        ),
    ]
