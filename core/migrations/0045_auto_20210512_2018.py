# Generated by Django 3.0.10 on 2021-05-12 20:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0044_auto_20210512_1924'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cumsmodel',
            name='fecha_vencimiento',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha vencimiento'),
        ),
    ]