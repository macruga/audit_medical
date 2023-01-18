# Generated by Django 3.0.10 on 2021-03-24 02:27

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0024_auto_20210324_0215'),
    ]

    operations = [
        migrations.AlterField(
            model_name='departamentomodel',
            name='description',
            field=models.CharField(help_text='Descripcion departamento', max_length=60, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces]),
        ),
    ]