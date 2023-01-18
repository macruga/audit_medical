from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces
#importar modelos de otros paquetes

# Modelo del estado del contrato
class estadoContratoModel(models.Model):
    '''
    Modelo de los posibles estados del contrato
    
    Attributes
    ----------
    description: string
        Descripcion del estado del contrato
    '''
    description = models.CharField(
        max_length=10,
        help_text='Descripción del estado del contrato',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_estado_contrato', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'contratacion'