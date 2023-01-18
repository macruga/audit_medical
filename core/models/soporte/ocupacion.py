from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits, onlyCharactersSpacesAndPunctuation

class OcupacionModel(models.Model):
    '''
    Modelo de la relación (Objeto) Ocupación que contiene los códigos del CIUO 08 de
    la Organización Internacional del Trabajo (OIT)

    Attributes
    ----------
    codigo: int
        Entero de cuatro digitos que represetna una ocupación según la OIT
    description: str
        descripción de la ocupación según la OIT
    '''

    codigo = models.PositiveIntegerField(
        help_text='Codigo de la ocupación',
        unique=True,
        null=False,
        blank=False,
        validators= [
            onlyDigits,
        ]
    )
    
    description = models.CharField(
        max_length=180,
        help_text='Ocupación',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
            ]
    )
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )

    class Meta:
        app_label = 'core'