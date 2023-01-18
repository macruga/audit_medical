# Generated by Django 3.0.10 on 2021-04-05 16:25

import core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0035_auto_20210327_0121'),
        ('contratacion', '0002_tarifariocontratadomodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='contratacionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_servicio', models.CharField(help_text='Código del servicio contratado', max_length=50, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndDigits])),
                ('porcentaje', models.DecimalField(decimal_places=1, help_text='Porcentaje del contrato, valor entre 0 y 100 con un digito decimal', max_digits=5, validators=[core.validators.noSpacesStartEnd, core.validators.onlyDigitsAndPoints])),
                ('fecha_inicio', models.DateField(help_text='Fecha de inicio de la contratación', verbose_name=())),
                ('fecha_fin', models.DateField(help_text='Fecha de finalización de la contratación', verbose_name=())),
                ('contratado', models.BooleanField(help_text='Si o No')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
                ('estado_contrato_id', models.ForeignKey(db_column='estado_contrato_id', help_text='Estado del contrato', on_delete=django.db.models.deletion.PROTECT, related_name='contratacion_estado_contrato', to='contratacion.estadoContratoModel')),
                ('ips_id', models.ForeignKey(db_column='ips_id', help_text='ips de la contratacion', on_delete=django.db.models.deletion.PROTECT, related_name='contratacion_ips', to='core.IpsModel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_contratacion', to=settings.AUTH_USER_MODEL)),
                ('tarifario_contratado_id', models.ForeignKey(db_column='tarifario_contratado_id', help_text='Tipo de tarifario contratado', on_delete=django.db.models.deletion.PROTECT, related_name='contratacion_tarifario_contratado', to='contratacion.tarifarioContratadoModel')),
            ],
        ),
    ]
