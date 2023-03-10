# Generated by Django 3.0.10 on 2021-03-19 02:41

import core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0013_codigosconsultamodel'),
        ('rips', '0022_auto_20210319_0241'),
    ]

    operations = [
        migrations.CreateModel(
            name='ApModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_factura', models.CharField(help_text='Numero de la Factura', max_length=30, validators=[core.validators.facturaType])),
                ('numero_identifacion_usuario', models.CharField(help_text='Numero de identificación del usuario', max_length=16, validators=[core.validators.onlyCharactersAndDigits])),
                ('fecha_procedimiento', models.DateField(verbose_name='Fecha Procedimiento')),
                ('numero_autorizacion', models.CharField(help_text='Número de autorización', max_length=20, validators=[core.validators.facturaType])),
                ('valor_procedimiento', models.DecimalField(decimal_places=2, default=0.0, help_text='Valor del procedimiento', max_digits=20)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('active', models.BooleanField(default=True)),
                ('ambito_procedimiento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ambito_procidimiento_ap', to='rips.AmbitoProcedimientoModel')),
                ('codigo_diagnostico_principal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='diagnostico_principal_procedimientos', to='core.Cie10Model')),
                ('codigo_personal_atiende', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='ambito_procidimiento_procedimientos', to='rips.PersonalAtencionModel')),
                ('codigo_prestador', models.ForeignKey(help_text='Codigo habilitacion del prestador', on_delete=django.db.models.deletion.CASCADE, related_name='codigo_prestador_ap', to='core.IpsModel')),
                ('codigo_procedimiento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cups_ap', to='core.CupsModel')),
                ('complicacion', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='complicacion_procedimientos', to='core.Cie10Model')),
                ('diagnostico_relacionado', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='diagnostico_relacionado_procedimientos', to='core.Cie10Model')),
                ('finalidad_procedimiento', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='finalidad_procidimiento_procedimientos', to='rips.FinalidadProcedimientoModel')),
                ('forma_realizacion_acto_cx', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='forma_realizacion_acto_quirurgico_procedimientos', to='rips.FormaActoCxModel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_create_af', to=settings.AUTH_USER_MODEL)),
                ('tipo_identificacion_usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tipo_identificacion_ap', to='core.TipoDocumentoModel')),
            ],
        ),
        migrations.AddIndex(
            model_name='apmodel',
            index=models.Index(fields=['numero_factura'], name='numero_fac_ap_idx'),
        ),
        migrations.AddIndex(
            model_name='apmodel',
            index=models.Index(fields=['codigo_prestador'], name='codigo_prestador_ap_idx'),
        ),
        migrations.AddIndex(
            model_name='apmodel',
            index=models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_ap_idx'),
        ),
        migrations.AddIndex(
            model_name='apmodel',
            index=models.Index(fields=['codigo_procedimiento'], name='codigo_procedimiento_ap_idx'),
        ),
        migrations.AddConstraint(
            model_name='apmodel',
            constraint=models.UniqueConstraint(fields=('numero_factura', 'codigo_prestador', 'numero_identifacion_usuario', 'codigo_procedimiento'), name='registro proc unico'),
        ),
    ]
