# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate
# importar los elementos de las otras bases de datos
from atencion_hc.models.atencion import atencionModel
from atencion_hc.models.imagen_diagnostica_ordenada_atencion import imagenDiagnosticaOrdenadaModel



# Modelo del reporte de imagenología asociado a la atención
class reporteImagenologiaModel(models.Model):
    '''
    Modelo de la relación (objeto) reporte de imagenologia

    Attributes
    ----------
    id: long
        Identificador del reporte de imagenologia
    atencion_id: int
        Identificador de la atención a la que se asocia el reporte de imagenologia
    imagen_dx_id: int
        Identificador de la imagen diagnóstica ordenada asociado a la atención
    description: str
        Descripcion del reporte de imagenología
    fecha_reporte: date
        fecha en la que se reporta el resultado de imagenología
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='reporte_imagenologia_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    imagen_dx_id = models.ForeignKey(
        imagenDiagnosticaOrdenadaModel, 
        related_name='reporte_imagenologia_imagen_ordenada', 
        on_delete=models.PROTECT,
        db_column="imagen_dx_id"
        )

    description = models.CharField(
        max_length=120,
        help_text='Descripción reporte de imagenología',
        unique=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )
    
    fecha_reporte = models.DateField(
        ("Fecha reporte de imagenología"), 
        auto_now=False, 
        auto_now_add=False,
        null=False,
        validators = [
            currentDate
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_reporte_imagenologia_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
