# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import currentDate, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation
# importar los elementos de las otras bases de datos
from atencion_hc.models.atencion import atencionModel
from core.models.soporte.cups import CupsModel


# Modelo de los peocedimientos ordenados en la atención
class procedimientoOrdenadoModel(models.Model):
    '''
    Modelo de la relación (objeto) procedimiento ordenado

    Attributes
    ----------
    id: long
        Identificador del procedimeinto ordenado en al atención
    atencion_id: int
        Identificador de la atención a la que se asocia el procedimiento ordenado
    codigo_cups: int
        Codigo del procedimiento ordenado
    fecha_orden: date
        fecha en la que fue ordenado el procedimiento
    description: str
        Descripción de la orden del procedimiento
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='procedimiento_ordenado_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    codigo_cups = models.ForeignKey(
        CupsModel, 
        related_name='procedimiento_ordenado_cups', 
        on_delete=models.PROTECT,
        db_column="cups_id"
        )

    fecha_orden = models.DateField(
        ("Fecha orden procedimiento"), 
        auto_now=False, 
        auto_now_add=False,
        null=False,
        validators = [
            currentDate
        ]
    )
    
    description = models.CharField(
        max_length=120,
        help_text='Descripción procedimiento ordenado',
        unique=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_procedimiento_ordenado_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
            