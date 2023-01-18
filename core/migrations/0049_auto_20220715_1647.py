# Generated by Django 3.0.10 on 2022-07-15 16:47

import core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0048_usermodel_group_ips'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='phone',
            field=models.CharField(default=111111111, help_text='Telefono usuario', max_length=30, validators=[core.validators.phoneValidator]),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='cargo',
            field=models.CharField(blank=True, help_text='Cargo usuario', max_length=200, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces]),
        ),
        migrations.AlterField(
            model_name='usermodel',
            name='empresa',
            field=models.CharField(blank=True, help_text='Empresa a la que pertenece el usuario', max_length=200, null=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces]),
        ),
    ]