from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits


class PaisModel(models.Model):
    """
    Modelo de los paises

    Attributes
    ----------
    codigo: int
        Código telefónico del pais
    iso2: string
        Código identificación ISO2 del país
    iso3: string
        Código identificación ISO3 del país
    nombre: string
        Nombre del país
    """
    codigo = models.PositiveIntegerField(
        null=False,
        help_text='Codigo del pais',
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )
    
    iso2 = models.CharField(
        max_length=2,
        help_text='Código identificación ISO2 del país',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    iso3 = models.CharField(
        primary_key=True,
        max_length=3,
        help_text='Código identificación ISO3 del país',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    description = models.CharField(
        max_length=60,
        help_text='Descripcion (nombre) Pais',
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