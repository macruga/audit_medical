from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces
#importar modelos de otros paquetes

# Modelo de los tipos de pqrs
class tipoPqrsModel(models.Model):
    '''
    Modelo de los tipos de PQRS
    
    Attributes
    ----------
    description: string
        Descripcion del tipo de PQRS
    '''
    description = models.CharField(
        max_length=20,
        help_text='Descripción del tipo de PQRS',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_tipo_pqrs', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'pqrs'