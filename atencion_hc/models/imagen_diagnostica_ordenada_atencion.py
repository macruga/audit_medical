# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, onlyDigitsAndPoints, onlyDigits, currentDate
# importar los elementos de las otras bases de datos
from atencion_hc.models.atencion import atencionModel
from core.models.soporte.cups import CupsModel


# Modelo de las imágenes diagnósticas ordenadas en una atención
class imagenDiagnosticaOrdenadaModel(models.Model):
    '''
    Modelo de la relación (objeto) imagen diagnóstica ordenada en la atención

    Attributes
    ----------
    id: long
        Identificador de la imagen diagnóstica ordenada
    atencion_id: int
        Identificador de la atención a la que se asocia la imagen diagnóstica ordenada
    codigo_cups: int
        codigo de la imagen diagnóstica ordenada en la relacion CUPS
    description: str
        Descripcion de la imagen diagnóstica que se ordena
    fecha_orden: date
        fecha en la que fue ordenada la imagen diagnóstica
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='imagen_diagnostica_ordenada_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    codigo_cups = models.ForeignKey(
        CupsModel, 
        related_name='imagen_diagnostica_ordenada_cups', 
        on_delete=models.PROTECT,
        db_column="cups_id"
        )

    description = models.TextField(
        max_length=150,
        help_text='Descripción de la imagen diagnóstica ordenada',
        unique=False,
        null=True,
        blank=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
            ]
    )
    
    fecha_orden = models.DateField(
        ("Fecha orden imagen diagnóstica"), 
        auto_now=False, 
        auto_now_add=False,
        null=False,
        validators = [
            currentDate
        ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_imagen_diagnostica_ordenada_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
