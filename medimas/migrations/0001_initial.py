# Generated by Django 3.0.10 on 2021-04-07 21:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='uploadFileConcurrenciaModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(upload_to='.')),
                ('procesado', models.BooleanField(default=False)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name=())),
                ('active', models.BooleanField(default=True)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='user_create_file', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
