from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits

# Modelo de la escolaridad
class EscolaridadModel(models.Model):
    description = models.CharField(
        max_length=50,
        help_text='Descripción de la Escolaridad',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )

    class Meta:
        app_label = 'core'