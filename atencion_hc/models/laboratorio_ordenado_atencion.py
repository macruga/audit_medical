# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate
# importar los elementos de las otras bases de datos
from atencion_hc.models.atencion import atencionModel
from core.models.soporte.cups import CupsModel


# Modelo de los laboratorios ordenados en la atención
class laboratorioOrdenadoModel(models.Model):
    '''
    Modelo de la relación (objeto) laboratorio ordenado

    Attributes
    ----------
    id: long
        Identificador del laboratorio ordenado en la atención
    atencion_id: int
        Identificador de la atención a la que se asocia el laboratorio ordenado
    codigo_cups: int
        Codigo del laboratorio ordenado
    fecha_orden: date
        fecha en la que fue ordenado el laboratorio
    description: str
        Descripción de la orden del laboratorio
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='laboratorio_ordenado_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    codigo_cups = models.ForeignKey(
        CupsModel, 
        related_name='laboratorio_ordenado_cups', 
        on_delete=models.PROTECT,
        db_column="cups_id"
        )

    fecha_orden = models.DateField(
        ("Fecha orden laboratorio"), 
        auto_now=False, 
        auto_now_add=False,
        null=False,
        validators = [
            currentDate
        ]
    )
    
    description = models.CharField(
        max_length=120,
        help_text='Descripción laboratorio ordenado',
        unique=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_laboratorio_ordenado_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
            