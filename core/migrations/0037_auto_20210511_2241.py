# Generated by Django 3.0.10 on 2021-05-11 22:41

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0036_paismodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ipsmodel',
            name='ips',
            field=models.CharField(help_text='Nombre de la IPS', max_length=200, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces]),
        ),
    ]
