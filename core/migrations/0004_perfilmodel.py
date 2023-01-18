# Generated by Django 3.0.10 on 2021-03-19 01:41

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_moduloapp'),
    ]

    operations = [
        migrations.CreateModel(
            name='PerfilModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('read', models.BooleanField(default=True, help_text='Autorizacion para consultas GET del modelo')),
                ('write', models.BooleanField(default=False, help_text='Autorizacion GET del modelo')),
                ('update', models.BooleanField(default=False, help_text='Autorizacion POST del modelo')),
                ('options', models.BooleanField(default=True, help_text='Autorizacion PUT del modelo')),
                ('delete', models.BooleanField(default=False, help_text='Autorizacion DELETE del modelo')),
                ('head', models.BooleanField(default=True, help_text='Autorizacion HEAD del modelo')),
                ('patch', models.BooleanField(default=False, help_text='Autorizacion PATCH del modelo')),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.GrupoPerfil')),
                ('modulo', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.ModuloApp')),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_prerfil', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]