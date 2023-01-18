# Generated by Django 3.0.10 on 2021-03-19 01:46

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_ipsmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoDocumentoModel',
            fields=[
                ('codigo', models.CharField(help_text='Tipo de Identificacion', max_length=2, primary_key=True, serialize=False, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharacters])),
                ('description', models.CharField(help_text='Descripcion', max_length=50, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
