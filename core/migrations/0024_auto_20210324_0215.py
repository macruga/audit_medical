# Generated by Django 3.0.10 on 2021-03-24 02:15

import core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0023_municipiomodel_departamento_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='zonaresidenciamodel',
            name='latitud',
            field=models.DecimalField(decimal_places=7, default=1, help_text='latitud de la zona de residencia', max_digits=11, validators=[core.validators.noSpacesStartEnd, core.validators.onlyDigitsAndPoints]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zonaresidenciamodel',
            name='longitud',
            field=models.DecimalField(decimal_places=7, default=0, help_text='longitud de la zona de residencia', max_digits=11, validators=[core.validators.noSpacesStartEnd, core.validators.onlyDigitsAndPoints]),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zonaresidenciamodel',
            name='municipio_id',
            field=models.ForeignKey(db_column='municipio_id', default=0, help_text='Código del municipio', on_delete=django.db.models.deletion.PROTECT, related_name='zona_residencia_municipio', to='core.MunicipioModel'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='zonaresidenciamodel',
            name='tipo',
            field=models.CharField(default='', help_text='tipo de zona residencia', max_length=20, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='zonaresidenciamodel',
            name='description',
            field=models.CharField(help_text='Descripcion codigo zona residencia', max_length=50, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces]),
        ),
    ]