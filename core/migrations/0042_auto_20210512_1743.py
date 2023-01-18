# Generated by Django 3.0.10 on 2021-05-12 17:43

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0041_auto_20210512_1738'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cumsmodel',
            name='fecha_expedicion',
            field=models.CharField(blank=True, help_text='Fecha expedicion', max_length=20, null=True, validators=[core.validators.noSpacesStartEnd]),
        ),
    ]
