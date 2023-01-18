# Generated by Django 3.0.10 on 2021-03-19 01:40

import core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20210319_0137'),
    ]

    operations = [
        migrations.CreateModel(
            name='ModuloApp',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('modulo', models.CharField(help_text='Codigo o nombre del modulo', max_length=100, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharacters])),
                ('descripcion', models.CharField(help_text='Descripcion del modulo', max_length=200, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharactersAndSpaces])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_modulo_app', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
