# Generated by Django 3.0.10 on 2021-03-24 03:54

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0028_auto_20210324_0352'),
    ]

    operations = [
        migrations.AlterField(
            model_name='zonaresidenciamodel',
            name='codigo',
            field=models.CharField(help_text='Codigo zona residencia', max_length=10, primary_key=True, serialize=False, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharacters]),
        ),
    ]
