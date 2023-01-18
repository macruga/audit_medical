# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate
# importar los elementos de las otras bases de datos
from atencion_hc.models.atencion import atencionModel
from core.models.soporte.cie10 import Cie10Model

# Modelo de las evoluciones en la atención
class evolucionModel(models.Model):
    '''
    Modelo de la relación (objeto) laboratorio ordenado

    Attributes
    ----------
    id: long
        Identificador del laboratorio ordenado en la atención
    atencion_id: int
        Identificador de la atención a la que se asocia el laboratorio ordenado
    fecha_evolucion: date
        fecha en la que fue realizada la evolucion
    diagnostico_principal: int
        Identificador del diagnóstico principal, código CIE10
    description: str
        Descripción de la orden del laboratorio
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='evolucion_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    fecha_evolucion = models.DateField(
        (), 
        auto_now=False, 
        auto_now_add=False,
        validators = [
            currentDate
        ]
    )

    diagnostico_principal = models.ForeignKey(
        Cie10Model, 
        related_name='evolucion_diagnostico_principal', 
        on_delete=models.PROTECT,
        db_column="diagnostico_principal_id"
        )
    
    description = models.TextField(
        help_text='Descripción de la evolución',
        unique=False,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )
    

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_evolucion_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
