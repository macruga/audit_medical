# Generated by Django 3.0.10 on 2021-03-24 02:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0022_auto_20210323_2145'),
    ]

    operations = [
        migrations.AddField(
            model_name='municipiomodel',
            name='departamento_id',
            field=models.ForeignKey(db_column='departamento_id', default=1, help_text='Código del departamento', on_delete=django.db.models.deletion.PROTECT, related_name='municipio_departamento', to='core.DepartamentoModel'),
            preserve_default=False,
        ),
    ]
