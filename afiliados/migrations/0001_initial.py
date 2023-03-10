# Generated by Django 3.0.10 on 2022-09-05 21:31

import core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0054_estadospacientemodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='afiliadoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identificacion', models.CharField(help_text='Identificacion del afiliado', max_length=100, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndDigits])),
                ('nombres', models.CharField(help_text='Nombres del afiliado', max_length=100, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('primer_apellido', models.CharField(help_text='Primer apellido', max_length=100, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('segundo_apellido', models.CharField(help_text='Segundo apellido', max_length=100, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('fecha_nacimiento', models.DateField(verbose_name='Fecha Nacimiento')),
                ('direccion', models.CharField(blank=True, help_text='dirección de residencia del afiliado', max_length=220, null=True, validators=[core.validators.noSpacesStartEnd])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
                ('codigo_departamento', models.ForeignKey(blank=True, db_column='departamento', help_text='Departamento donde reside el afiliado', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_departamento', to='core.DepartamentoModel')),
                ('codigo_municipio', models.ForeignKey(blank=True, db_column='municipio', help_text='Municipio donde reside el afiliado', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_municipio', to='core.MunicipioModel')),
                ('codigo_zona_residencial', models.ForeignKey(blank=True, db_column='zona_residencial', help_text='Zona donde reside el afiliado', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_zona_residencial', to='core.ZonaResidenciaModel')),
                ('discapacidad', models.ForeignKey(blank=True, db_column='discapacidad', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_discapacidades', to='core.CifModel')),
                ('escolaridad', models.ForeignKey(blank=True, db_column='escolaridad', help_text='Nivel de escolaridad', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_nivel_escolaridad', to='core.EscolaridadModel')),
                ('estado_civil', models.ForeignKey(blank=True, db_column='estado_civil', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_estado_civil', to='core.EstadoCivilModel')),
                ('estado_paciente', models.ForeignKey(db_column='estado_paciente', default='N', help_text='Estado de paciente o vital del afiliado', on_delete=django.db.models.deletion.PROTECT, related_name='estado_paciente_afiliado', to='core.EstadosPacienteModel')),
                ('grupo_poblacional', models.ForeignKey(blank=True, db_column='grupo_poblacional', help_text='Grupo poblacional', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_grupo_poblacional', to='core.GrupoPoblacionalModel')),
                ('ocupacion_actual', models.ForeignKey(blank=True, db_column='ocupacion_actual', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_ocupacion', to='core.OcupacionModel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_afiliado', to=settings.AUTH_USER_MODEL)),
                ('pertenencia_etnica', models.ForeignKey(blank=True, db_column='pertenencia_etnica', help_text='Pertenencia étnica', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_pertenencia_etnica', to='core.OrigenEtnicoModel')),
                ('sexo', models.ForeignKey(db_column='sexo', on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_sexo', to='core.SexoModel')),
                ('tipo_identificacion', models.ForeignKey(db_column='tipo_identificacion', help_text='Tipo de identificación del afiliado', on_delete=django.db.models.deletion.CASCADE, related_name='afiliado_tipo_identificacion', to='core.TipoDocumentoModel')),
                ('vulnerabilidad', models.ForeignKey(blank=True, db_column='vulnerabilidad', help_text='Nivel de vulnerabilidad', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_vulnerabilidad', to='core.VulnerabilidadModel')),
            ],
        ),
        migrations.CreateModel(
            name='regimenModel',
            fields=[
                ('id', models.CharField(help_text='Sigla del regimen', max_length=3, primary_key=True, serialize=False, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharacters])),
                ('description', models.CharField(help_text='Descripción del regimen', max_length=50, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharacters])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_regimen_afiliacion', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='CohorteAfiliadoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_ingreso', models.DateField(blank=True, help_text='Fecha de ingreso del afiliado a la cohorte', null=True, validators=[core.validators.currentDate])),
                ('status', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
                ('afiliado_id', models.ForeignKey(db_column='afiliado_id', help_text='identificador del afiliado', on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_cohorte_afiliado', to='afiliados.afiliadoModel')),
                ('cohorte_id', models.ForeignKey(db_column='cohorte_id', help_text='Cohorte del afiliado', on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_cohorte_cohorte', to='core.CohorteModel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_cohorte_afiliado', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='aseguradorasModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='Nombre de la Aseguradora', max_length=50, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('nit', models.CharField(help_text='NIT de la Aseguradora', max_length=50, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyDigits])),
                ('habilitado', models.BooleanField(default=True, help_text='Habilitado')),
                ('telefono', models.CharField(help_text='Telefono Movil 1', max_length=50, validators=[core.validators.noSpacesStartEnd, core.validators.onlyDigits])),
                ('email', models.EmailField(help_text='Correo Electrónico', max_length=100, validators=[core.validators.noSpacesStartEnd])),
                ('active', models.BooleanField(default=True)),
                ('created', models.DateField(auto_now_add=True, verbose_name=())),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_aseguradoras_afiliacion', to=settings.AUTH_USER_MODEL)),
                ('regimen_id', models.ForeignKey(db_column='regimen_id', help_text='regimen de la EAPB', on_delete=django.db.models.deletion.PROTECT, related_name='aseguradora_regimen', to='afiliados.regimenModel')),
            ],
        ),
        migrations.CreateModel(
            name='AfiliacionModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_afiliacion', models.DateField(verbose_name='Fecha Afiliacion')),
                ('fecha_vencimiento', models.DateField(verbose_name='Fecha vencimiento afiliacion')),
                ('status_afiliacion', models.BooleanField(default=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
                ('afiliado_id', models.ForeignKey(db_column='afiliado_id', help_text='identificador del afiliado', on_delete=django.db.models.deletion.PROTECT, to='afiliados.afiliadoModel')),
                ('aseguradora_id', models.ForeignKey(db_column='aseguradora_id', on_delete=django.db.models.deletion.PROTECT, related_name='aseguradora_afiliacion', to='afiliados.aseguradorasModel')),
                ('ips_primaria', models.ForeignKey(db_column='ips_primaria', on_delete=django.db.models.deletion.PROTECT, related_name='ips_primaria', to='core.IpsModel')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_afiliacion', to=settings.AUTH_USER_MODEL)),
                ('regimen', models.ForeignKey(db_column='regimen_id', on_delete=django.db.models.deletion.PROTECT, related_name='regimen_afiliacion', to='afiliados.regimenModel')),
            ],
        ),
        migrations.AddConstraint(
            model_name='afiliacionmodel',
            constraint=models.UniqueConstraint(condition=models.Q(status_afiliacion=True), fields=('afiliado_id', 'status_afiliacion'), name='Solo una afiliacion activa por paciente'),
        ),
    ]
