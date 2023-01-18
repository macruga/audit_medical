# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharacters
# importar los elementos de las otras bases de datos


# modelo de ordenes de reingreso para la Auditoria en concurrencia
class ordenReingresoModel (models.Model):
    '''
    Modelo de la relación de ordenes de reingreso en la auditoría

    Attributes
    ----------
    description: str
        La orden de reingreso en el procedimiento para la auditoría
    '''
    description = models.CharField(
        max_length=50,
        help_text='Orden reingreso',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_orden_reingreso_auditoria', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'auditoria'
