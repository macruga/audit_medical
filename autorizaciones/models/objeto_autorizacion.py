from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces
#importar modelos de otros paquetes
from core.models.soporte.cups import CupsModel
from core.models.soporte.cums import CumsModel

from autorizaciones.models.autorizacion import autorizacionModel

# Modelo del objeto de la Autorizacion
class objetoAutorizacionModel(models.Model):
    '''
    Modelo de la relacion para indicar los objetos relacionados con una autorización
    
    Attributes
    ----------
    autorizacion_id: long
        Relación con la autorización a la que pertence este objeto
    codigo_cups_id: long
        Relación con el procedimiento de la autorizacion
    codigo_cums_id: long
        Relación con el medicamento de la autorizacion
    cantidad_autorizada: integer
        Cantidad del objeto autorizado
    '''
    
    autorizacion_id = models.ForeignKey(
        autorizacionModel,
        help_text="Autorización ",
        related_name="autorizacion_objeto_autorizacion",
        on_delete=models.PROTECT,
        db_column='autorizacion_id'
    )
    
    codigo_cups_id = models.ForeignKey(
        CupsModel,
        help_text="Código CUPS autorizado",
        related_name="autorizacion_objeto_cups",
        on_delete=models.PROTECT,
        db_column='codigo_cups_id',
        null=True
    )
    
    codigo_cums_id = models.ForeignKey(
        CumsModel,
        help_text="Código CUMS autorizado",
        related_name="autorizacion_objeto_cums",
        on_delete=models.PROTECT,
        db_column='codigo_cums_id',
        null=True
    )
    
    cantidad_autorizada = models.PositiveSmallIntegerField(
        help_text="Cantidad autorizada",
        validators=[MinValueValidator(1)]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_objeto_autorizacion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
    
    class Meta:
        app_label = 'autorizaciones'