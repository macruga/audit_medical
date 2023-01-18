from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits


class TipoDocumentoModel(models.Model):
    codigo = models.CharField(
        primary_key=True,
        max_length=2,
        help_text='Tipo de Identificacion',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
            ]
    )
    description = models.CharField(
        max_length=50,
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