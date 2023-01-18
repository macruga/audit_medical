# Generated by Django 3.0.10 on 2023-01-10 03:59

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TipoObjecionModel',
            fields=[
                ('codigo', models.CharField(help_text='Codigo objecion', max_length=4, primary_key=True, serialize=False, unique=True, validators=[core.validators.noSpacesStartEnd])),
                ('description', models.CharField(help_text='Descripcion objecion', max_length=250, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
