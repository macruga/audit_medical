# Generated by Django 3.0.10 on 2021-05-13 02:29

import core.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_perfilmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='CupsModel',
            fields=[
                ('codigo', models.CharField(help_text='Codigo CUPS', max_length=6, primary_key=True, serialize=False, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndDigits])),
                ('nombre', models.TextField(help_text='Nombre CUPS', max_length=300, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('seccion', models.CharField(help_text='Sección CUPS', max_length=120, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('uso_codigo_rips', models.CharField(blank=True, help_text='Uso código CUPS en tablas RIPS', max_length=5, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('qx', models.CharField(blank=True, help_text='Código CUPS quirúrgico', max_length=1, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('numero_minimo', models.IntegerField(blank=True, help_text='Número Mínimo CUPS', null=True, validators=[django.core.validators.MinValueValidator(0)])),
                ('numero_maximo', models.IntegerField(blank=True, help_text='Número Mínimo CUPS', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1000)])),
                ('dx_requerido', models.CharField(blank=True, help_text='Diagnóstico requerido CUPS', max_length=1, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('capitulo', models.CharField(help_text='Capítulo CUPS', max_length=100, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('fecha_actualizacion', models.DateField(blank=True, null=True, validators=[core.validators.currentDate], verbose_name='Fecha actualización')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_cups', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
