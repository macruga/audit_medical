# Generated by Django 3.0.10 on 2023-01-05 23:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('medicamentos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='medicamentomodel',
            name='asesor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='asesor_medicamentos', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='medicamentomodel',
            name='auditor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='auditor_medicamentos', to=settings.AUTH_USER_MODEL),
        ),
    ]
