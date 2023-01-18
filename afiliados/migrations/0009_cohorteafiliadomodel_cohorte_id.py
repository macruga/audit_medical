# Generated by Django 3.0.10 on 2022-09-19 21:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_auto_20220919_2138'),
        ('afiliados', '0008_remove_cohorteafiliadomodel_cohorte_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='cohorteafiliadomodel',
            name='cohorte_id',
            field=models.ForeignKey(db_column='cohorte_id', default='AAA', help_text='Cohorte del afiliado', on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_cohorte_cohorte', to='core.CohorteModel'),
            preserve_default=False,
        ),
    ]