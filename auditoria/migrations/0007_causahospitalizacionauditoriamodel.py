# Generated by Django 3.0.10 on 2021-06-15 22:53

import core.validators
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('auditoria', '0006_tiposfugamodel'),
    ]

    operations = [
        migrations.CreateModel(
            name='causaHospitalizacionAuditoriaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(help_text='Falla', max_length=260, validators=[core.validators.noSpacesStartEnd, core.validators.onlyCharacters])),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_causa_hospitalizacion', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
