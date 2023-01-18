# Generated by Django 3.0.10 on 2021-03-19 02:34

import core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rips', '0005_unidadedadmodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoUsuarioModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(help_text='Descripcion ambito del procedimiento', max_length=20, unique=True, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharacters])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_tipo_usuario', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]