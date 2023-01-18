from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits


class SexoModel(models.Model):
    codigo = models.CharField(
        primary_key=True,
        max_length=1,
        help_text='Caracter de Sexo',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
            ]
    )
    description = models.CharField(
        max_length=10,
        help_text='Descripcion',
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