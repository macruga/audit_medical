from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits


class DepartamentoModel(models.Model):
    codigo = models.CharField(
        primary_key=True,
        max_length=5,
        help_text='Codigo Departamento',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
            ]
    )
    description = models.CharField(
        max_length=60,
        help_text='Descripcion departamento',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )

    class Meta:
        app_label = 'core'