from django.db import models
from django.conf import settings
from core.validators import onlyCharacters, noSpacesStartEnd
from rips.models.tipo_archivo import TipoArchivoModel

# Modelo para la definicion de las reglas de validacion 
class reglasModel(models.Model):
    regla = models.CharField(
        primary_key=True,
        max_length=2,
        help_text='Codigo Archivo',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
            ]
    )
    description = models.CharField(
        max_length=200,
        help_text='Descripcion del tipo de archivo',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
            ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_regla', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )

    # Importante agregar esta clase meta en la creacion de cada modelo, para organizacion de la estructura de django
    class Meta: 
        app_label = 'rips'