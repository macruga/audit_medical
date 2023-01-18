# Generated by Django 3.0.10 on 2021-03-19 02:41

import core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0013_codigosconsultamodel'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rips', '0020_auto_20210319_0241'),
    ]

    operations = [
        migrations.CreateModel(
            name='AcModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_factura', models.CharField(help_text='Numero de la Factura', max_length=30, validators=[core.validators.facturaType])),
                ('numero_identifacion_usuario', models.CharField(help_text='Numero de identificación del usuario', max_length=16, validators=[core.validators.onlyCharactersAndDigits])),
                ('fecha_consulta', models.DateField(verbose_name='Fecha Consulta')),
                ('numero_autorizacion', models.CharField(help_text='Número de autorización', max_length=20, validators=[core.validators.facturaType])),
                ('valor_consulta', models.DecimalField(decimal_places=2, default=0.0, help_text='Valor de la consulta', max_digits=20)),
                ('valor_cuota_moderadora', models.DecimalField(decimal_places=2, default=0.0, help_text='Valor de la cuota moderadora', max_digits=20)),
                ('valor_neto_pagar', models.DecimalField(decimal_places=2, default=0.0, help_text='Valor neto a pagar', max_digits=20)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creacion')),
                ('codigo_causa_externa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='causa_externa_consulta', to='rips.CausaExternaModel')),
                ('codigo_consulta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='codigo_consulta_ac', to='core.CodigosConsultaModel')),
                ('codigo_diagnostico_principal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='diagnostico_principal_consulta', to='core.Cie10Model')),
                ('codigo_diagnostico_relacionado1', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='diagnostico_relacionado1_consulta', to='core.Cie10Model')),
                ('codigo_diagnostico_relacionado2', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='diagnostico_relacionado2_consulta', to='core.Cie10Model')),
                ('codigo_diagnostico_relacionado3', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='diagnostico_relacionado3_consulta', to='core.Cie10Model')),
                ('codigo_finalidad_consulta', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='finalidad_consulta_ac', to='rips.FinalidadConsultatoModel')),
                ('codigo_prestador', models.ForeignKey(help_text='Codigo habilitacion del prestador', on_delete=django.db.models.deletion.CASCADE, related_name='codigo_prestador_ac', to='core.IpsModel')),
                ('codigo_tipo_diagnostico_principal', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tipo_diagnostico_consulta', to='rips.TipoDxPrincipalModel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='affiles', to=settings.AUTH_USER_MODEL)),
                ('tipo_identificacion_usuario', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='tipo_identificacion_ac', to='core.TipoDocumentoModel')),
            ],
        ),
        migrations.AddIndex(
            model_name='acmodel',
            index=models.Index(fields=['numero_factura'], name='numero_fac_ac_idx'),
        ),
        migrations.AddIndex(
            model_name='acmodel',
            index=models.Index(fields=['codigo_prestador'], name='codigo_prestador_ac_idx'),
        ),
        migrations.AddIndex(
            model_name='acmodel',
            index=models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_ac_idx'),
        ),
        migrations.AddConstraint(
            model_name='acmodel',
            constraint=models.UniqueConstraint(fields=('numero_factura', 'codigo_prestador', 'numero_identifacion_usuario', 'codigo_finalidad_consulta', 'codigo_consulta'), name='registro consulta unico'),
        ),
    ]
