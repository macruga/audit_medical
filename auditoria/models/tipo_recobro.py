# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharacters
# importar los elementos de las otras bases de datos


# modelo de ordenes de reingreso para la Auditoria en concurrencia
class tipoRecobroModel (models.Model):
    '''
    Modelo de la relación de tipos de recobro en la auditoría

    Attributes
    ----------
    description: str
        El tipo de recobro en el procedimiento para la auditoría
    '''
    description = models.CharField(
        max_length=15,
        help_text='Tipo de recobro',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_tipo_recobro_auditoria', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'auditoria'
