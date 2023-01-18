# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate
# importar los elementos de las otras bases de datos
from atencion_hc.models.atencion import atencionModel
from core.models.soporte.cups import CupsModel

# Modelo de los insumos ordenados en la atención
class insumoOrdenadoModel(models.Model):
    '''
    Modelo de la relación (objeto) insumo ordenado

    Attributes
    ----------
    id: long
        Identificador del insumo ordenado
    atencion_id: int
        Identificador de la atención a la que se asocia el insumo ordenado
    codigo_cups: int
        Codigo del insumo ordenado
    fecha_orden: date
        fecha en la que fue ordenado el insumo
    description: str
        Descripción de la orden del insumo
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='insumo_ordenado_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    codigo_cups = models.ForeignKey(
        CupsModel, 
        related_name='insumo_ordenado_cups', 
        on_delete=models.PROTECT,
        db_column="cups_id"
        )

    fecha_orden = models.DateField(
        ("Fecha orden insumo"), 
        auto_now=False, 
        auto_now_add=False,
        null=False,
        validators = [
            currentDate
        ]
    )
    
    description = models.CharField(
        max_length=120,
        help_text='Descripción insumo ordenado',
        unique=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_insumo_ordenado_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
            