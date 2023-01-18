# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate
# importar los elementos de las otras bases de datos
from atencion_hc.models.atencion import atencionModel
from atencion_hc.models.laboratorio_ordenado_atencion import laboratorioOrdenadoModel



# Modelo del reporte de microbiología asociado a la atención
class reporteMicrobiologiaModel(models.Model):
    '''
    Modelo de la relación (objeto) reporte de microbiología

    Attributes
    ----------
    id: long
        Identificador del reporte de microbiologia
    atencion_id: int
        Identificador de la atención a la que se asocia el reporte de microbiologia
    laboratorio_id: int
        Identificador del laboratorio ordenado asociado a la atención
    description: str
        Descripcion del reporte de microbiologia
    fecha_reporte: date
        fecha en la que se reporta el resultado de microbiologia
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='reporte_microbiologia_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    laboratorio_id = models.ForeignKey(
        laboratorioOrdenadoModel, 
        related_name='reporte_microbiologia_laboratorio_ordenado', 
        on_delete=models.PROTECT,
        db_column="laboratorio_id"
        )

    description = models.CharField(
        max_length=120,
        help_text='Descripción reporte de microbiología',
        unique=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )
    
    fecha_reporte = models.DateField(
        ("Fecha reporte de microbiología"), 
        auto_now=False, 
        auto_now_add=False,
        null=False,
        validators = [
            currentDate
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_reporte_microbiologia_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
