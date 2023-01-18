# Generated by Django 3.0.10 on 2021-03-19 02:40

import core.validators
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rips', '0017_auto_20210319_0240'),
    ]

    operations = [
        migrations.CreateModel(
            name='AfIntermediaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo_prestador', models.CharField(help_text='Codigo del prestador', max_length=15, validators=[core.validators.onlyDigits])),
                ('prestador', models.CharField(blank=True, help_text='Nombre del prestador', max_length=200, null=True)),
                ('tipo_documento', models.CharField(blank=True, help_text='Tipo documento prestador', max_length=2, null=True)),
                ('numero_documento', models.CharField(blank=True, help_text='Numero del documento del prestador', max_length=16, null=True)),
                ('numero_factura', models.CharField(help_text='Numero de la Factura', max_length=30)),
                ('fecha_expedicion', models.CharField(blank=True, help_text='Fecha de expedicion de la factura', max_length=22, null=True)),
                ('fecha_inicio', models.CharField(blank=True, help_text='Fecha de inicio', max_length=22, null=True)),
                ('fecha_final', models.CharField(blank=True, help_text='Fecha final', max_length=22, null=True)),
                ('codigo_entidad', models.CharField(blank=True, help_text='Codigo de la Entidad administradora', max_length=30, null=True)),
                ('nombre_entidad', models.CharField(blank=True, help_text='Nombre de la Entidad administradora', max_length=200, null=True)),
                ('numero_contrato', models.CharField(blank=True, help_text='Numero contrato', max_length=40, null=True)),
                ('plan_beneficios', models.CharField(blank=True, help_text='Plan Beneficios', max_length=40, null=True)),
                ('numero_poliza', models.CharField(blank=True, default=0, help_text='Numero Poliza', max_length=40, null=True)),
                ('valor_pago_compartido', models.CharField(blank=True, help_text='Valor copago', max_length=15, null=True)),
                ('valor_comision', models.CharField(blank=True, help_text='Valor comision', max_length=15, null=True)),
                ('valor_descuentos', models.CharField(blank=True, help_text='Valor descuentos', max_length=15, null=True)),
                ('valor_neto_pagar', models.CharField(blank=True, help_text='Valor neto a pagar por la entidad contratante', max_length=40, null=True)),
                ('estado_validacion', models.IntegerField(default=0, help_text='Estado de la validacion del registro', validators=[django.core.validators.MinValueValidator(0), django.core.validators.MinValueValidator(100)])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='af_file_intermedia', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddIndex(
            model_name='afintermediamodel',
            index=models.Index(fields=['numero_factura'], name='numero_factura_int_idx'),
        ),
        migrations.AddIndex(
            model_name='afintermediamodel',
            index=models.Index(fields=['codigo_prestador'], name='codigo_prestador_int_idx'),
        ),
        migrations.AddIndex(
            model_name='afintermediamodel',
            index=models.Index(fields=['numero_documento'], name='numero_documento_int_idx'),
        ),
        migrations.AddConstraint(
            model_name='afintermediamodel',
            constraint=models.UniqueConstraint(fields=('codigo_prestador', 'numero_factura'), name='factura unica tabla intermedia'),
        ),
    ]