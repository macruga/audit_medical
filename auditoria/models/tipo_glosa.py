# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharacters, onlyAlphaNumeric, onlyCharactersAndSpaces, onlyCharactersSpacesAndPunctuation, onlyCharactersAndDigits, onlyDigits, onlyDigitsAndPoints, currentDate, rangeDate, facturaType
# importar los elementos de las otras bases de datos


# importar los elementos adicinales del paquete



# modelo de Tipos Glosa para la Auditoria
class tipoGlosaAuditoriaModel (models.Model):
    '''
    Modelo de la relación tipo de glosa en la auditoría

    Attributes
    ----------
    codigo: int
        Código del tipo de glosa
    description: str
        Descripción del tipo de glosa sobre el procedimiento en la auditoría
    '''
    codigo = models.PositiveIntegerField(
        primary_key=True,
        help_text='Codigo del tipo de glosa',
        unique=True,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )
    description = models.TextField(
        max_length=180,
        help_text='glosa',
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_tipo_glosa_auditoria', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}{}'.format( self.codigo, self.description)
    
    class Meta:
        app_label = 'auditoria'
