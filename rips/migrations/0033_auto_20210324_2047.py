# Generated by Django 3.0.10 on 2021-03-24 20:47

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rips', '0032_auto_20210319_0243'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ammodel',
            name='codigo_medicamento',
            field=models.CharField(help_text='Codigo medicamento', max_length=100, validators=[core.validators.facturaType]),
        ),
    ]
