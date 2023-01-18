# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharacters
# importar los elementos de las otras bases de datos


# modelo de Tipos de Soporte para la Auditoria
class tiposSoporteModel (models.Model):
    '''
    Modelo de la relación de tipos de soporte para la auditoría

    Attributes
    ----------
    description: str
        El soporte en el procedimiento para la auditoría
    '''
    description = models.CharField(
        max_length=50,
        help_text='Tipo de soporte',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_tipos_soporte_auditoria', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'auditoria'
