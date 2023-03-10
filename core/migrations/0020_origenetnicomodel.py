# Generated by Django 3.0.10 on 2021-03-23 20:20

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_ocupacionmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrigenEtnicoModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='Descripción del grupo étnico', max_length=50, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('active', models.BooleanField(default=True)),
            ],
        ),
    ]
