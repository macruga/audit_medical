# Generated by Django 3.0.10 on 2021-07-18 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0047_auto_20210513_0357'),
    ]

    operations = [
        migrations.AddField(
            model_name='usermodel',
            name='group_ips',
            field=models.ManyToManyField(help_text='Grupo de IPS asociadas al usuario', to='core.IpsModel'),
        ),
    ]
