from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits, facturaType


class CodigosConsultaModel(models.Model):
    codigo = models.CharField(
        primary_key=True,
        max_length=10,
        help_text='Codigo de la consulta',
        unique=False,
        null=False,
        validators=[
            facturaType
        ]
    )
    description = models.CharField(
        max_length=50,
        help_text='Descripcion del codigo de la consulta',
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