from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits, onlyDigitsAndPoints
from core.models.soporte.municipios import MunicipioModel

class ZonaResidenciaModel(models.Model):
    codigo = models.CharField(
        primary_key=True,
        max_length=10,
        help_text='Codigo zona residencia',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
            ]
    )

    description = models.CharField(
        max_length=100,
        help_text='Descripcion codigo zona residencia',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    municipio_id = models.ForeignKey(
        MunicipioModel, 
        help_text="Código del municipio", 
        related_name="zona_residencia_municipio", 
        on_delete=models.PROTECT,
        db_column="municipio_id"
        )

    tipo = models.CharField(
        max_length=20,
        help_text='tipo de zona residencia',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    
    latitud = models.DecimalField(
        help_text='latitud de la zona de residencia',
        max_digits=16,
        decimal_places=12,
        unique=False,
        null=True,
        blank=True,
        validators= [
            noSpacesStartEnd,
            onlyDigitsAndPoints,
        ]
    )

    longitud = models.DecimalField(
        help_text='longitud de la zona de residencia',
        max_digits=16,
        decimal_places=12,
        unique=False,
        null=True,
        blank=True,
        validators= [
            noSpacesStartEnd,
            onlyDigitsAndPoints,
        ]
    )
    
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )

    class Meta:
        app_label = 'core'