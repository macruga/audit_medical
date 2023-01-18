# Generated by Django 3.0.10 on 2021-05-13 02:53

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0045_auto_20210512_2018'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cupsmodel',
            name='seccion',
            field=models.CharField(blank=True, help_text='Sección CUPS', max_length=120, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces]),
        ),
    ]