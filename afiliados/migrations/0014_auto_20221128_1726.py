# Generated by Django 3.0.10 on 2022-11-28 17:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0055_auto_20220919_2138'),
        ('afiliados', '0013_auto_20221128_1723'),
    ]

    operations = [
        migrations.AlterField(
            model_name='afiliacionmodel',
            name='aseguradora_id',
            field=models.ForeignKey(db_column='aseguradora_id', on_delete=django.db.models.deletion.PROTECT, related_name='aseguradora_afiliacion', to='afiliados.AseguradorasModel'),
        ),
        migrations.AlterField(
            model_name='afiliacionmodel',
            name='regimen',
            field=models.ForeignKey(db_column='regimen_id', on_delete=django.db.models.deletion.PROTECT, related_name='regimen_afiliacion', to='afiliados.RegimenModel'),
        ),
        migrations.AlterField(
            model_name='aseguradorasmodel',
            name='regimen_id',
            field=models.ForeignKey(db_column='regimen_id', help_text='regimen de la EAPB', on_delete=django.db.models.deletion.PROTECT, related_name='aseguradora_regimen', to='afiliados.RegimenModel'),
        ),
        migrations.AlterField(
            model_name='cohorteafiliadomodel',
            name='cohorte_id',
            field=models.ForeignKey(db_column='cohorte_id', help_text='Cohorte del afiliado', on_delete=django.db.models.deletion.PROTECT, related_name='afiliado_cohorte_cohorte', to='core.CohorteModel'),
        ),
    ]
