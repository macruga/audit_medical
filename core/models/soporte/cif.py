from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharactersAndSpaces, onlyCharactersAndDigits

# Modelo de la CIF para la definición de discapacidades
class CifModel(models.Model):
    '''
    Modelo de la relación CIF clasificación Internacional del funcionamiento, de la discapacidad y de la salud
    https://apps.who.int/classifications/icfbrowser/Default.aspx,

    Ej: 
        b1100 -> b grupo principal
              -> 1 capítulo
              -> 1 subcapítulo
              -> 0 sección
              -> 0 subsección



    Attributes
    ----------
    codigo: str
        Código de la clasificación del funcionamiento, de la discapacidad y de la salud
    titulo: str
        Título o nombre de la clasificación del funcionamiento, de la discapacidad y de la salud

    '''
    codigo = models.CharField(
        primary_key=True,
        max_length=6,
        help_text='Codigo CIF',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
    titulo = models.CharField(
        max_length=250,
        help_text='Descripcion CIF',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_cif', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )
        
    class Meta: 
        app_label = 'core'