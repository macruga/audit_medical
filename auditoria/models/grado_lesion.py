# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharacters
# importar los elementos de las otras bases de datos

# importar los elementos adicionales del paquete

# modelo de grado de lesion para la Auditoria
class gradoLesionuditoriaModel (models.Model):
    '''
    Modelo de la relación Grado de lesión auditoría

    Attributes
    ----------
    description: str
        Relación al grado de lesión [LEVE, MODERADO, GRAVE]
    '''
    description = models.TextField(
        max_length=260,
        help_text='Grado de lesión',
        # unique=True, produce un error por el maximo numero de caracteres
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_grado_lesion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'auditoria'
