# Generated by Django 3.0.10 on 2021-05-12 19:24

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0043_auto_20210512_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cumsmodel',
            name='cantidad',
            field=models.CharField(blank=True, help_text='Cantidad', max_length=20, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyDigitsAndPoints]),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='concentracion',
            field=models.CharField(blank=True, help_text='Concentracion', max_length=5, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharacters]),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='descripcion_comercial',
            field=models.TextField(blank=True, help_text='Descripcion comercial', max_length=800, null=True, validators=[core.validators.noSpacesStartEnd]),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='estado_registro',
            field=models.CharField(blank=True, help_text='Estado registro', max_length=50, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharacters]),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='fecha_activo',
            field=models.DateField(blank=True, null=True, validators=[core.validators.currentDate], verbose_name='Fecha activo'),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='fecha_expedicion',
            field=models.DateField(blank=True, null=True, validators=[core.validators.currentDate], verbose_name='Fecha expedición'),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='fecha_inactivo',
            field=models.DateField(blank=True, null=True, validators=[core.validators.currentDate], verbose_name='Fecha inactivo'),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='fecha_vencimiento',
            field=models.DateField(blank=True, null=True, validators=[core.validators.currentDate], verbose_name='Fecha vencimiento'),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='forma_farmaceutica',
            field=models.CharField(blank=True, help_text='Forma farmaceutica', max_length=150, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces]),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='principio_activo',
            field=models.TextField(blank=True, help_text='Principio activo', max_length=450, null=True, validators=[core.validators.noSpacesStartEnd]),
        ),
        migrations.AlterField(
            model_name='cumsmodel',
            name='via_administracion',
            field=models.CharField(blank=True, help_text='Via administracion', max_length=50, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharacters]),
        ),
    ]
