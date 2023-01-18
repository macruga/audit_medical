from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces
#importar modelos de otros paquetes


# Modelo del tarifario contratado
class tarifarioContratadoModel(models.Model):
    '''
    Modelo de la entidad que representa el tarifario contratado
    
    Attributes
    ----------
    codigo: string
        Codigo del tarifario
    description: string
        Descripción del tarifario
    '''
    codigo = models.CharField(
        primary_key=True,
        max_length=10,
        help_text='Código del tarifario contratado',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
        
    description = models.CharField(
        max_length=200,
        help_text='Descripción del tarifario contratado',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_tarifario_contratado', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )
    
    class Meta:
        app_label = 'contratacion'