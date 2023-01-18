# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, onlyDigitsAndPoints, onlyDigits, currentDate
# importar los elementos de las otras bases de datos
from atencion_hc.models.atencion import atencionModel
from core.models.soporte.cums import CumsModel



# Modelo de los medicamentos ordenados en una atención
class medicamentoOrdenadoModel(models.Model):
    '''
    Modelo de la relación (objeto) medicamento ordenado en la atención

    Attributes
    ----------
    id: long
        Identificador del medicamento ordenado
    atencion_id: int
        Identificador de la atención a la que se asocia el medicamento ordenado
    nombre_generico: str
        Nombre generico del medicamento ordenado
    codigo_cums: int
        codigo de medicamento en la relacion CUMS
    numero_total: int
        cantidad del medicamento que se ordena
    cantidad_dosis: int
        cuantas debe usarse en una dosis
    frecuencia_dosis: int
        cada cuanto se debe consumir el medicamento ordenado 
    duracion_tratamiento: int
        numero total de dias que dura el tratameinto
    recomendacion: str
        recomendaciones adicionales o instrucciones especificas del tratamiento
    fecha_orden: date
        fecha en la que fue ordenado el medicamento
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='medicamento_ordenado_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    nombre_generico = models.CharField(
        max_length=50,
        help_text='Nombre genérico del medicamento',
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
            ]
    )

    codigo_cums = models.ForeignKey(
        CumsModel, 
        related_name='medicamento_ordenado_cums',
        on_delete=models.PROTECT,
        db_column="cums_id"
        )

    numero_total = models.PositiveIntegerField(
        help_text='Cantidad de unidades del medicamento',
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )

    cantidad_dosis = models.DecimalField(
        help_text='Cantidad de una dosis del medicamento',
        max_digits=4,
        decimal_places=1,
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyDigitsAndPoints,
        ]
    )

    frecuencia_dosis = models.CharField(
        max_length=50,
        help_text='frecuancia de dosis del medicamento',
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
            ]
    )

    duracion_tratamiento = models.PositiveIntegerField(
        help_text='Duración en días deltratamiento',
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )

    recomendacion = models.TextField(
        max_length=250,
        help_text='Recomendaciones de la administración del medicamento',
        unique=False,
        null=True,
        blank=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
            ]
    )
    
    fecha_orden = models.DateField(
        ("Fecha orden medicamento"), 
        auto_now=False, 
        auto_now_add=False,
        null=False,
        validators = [
            currentDate
        ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_medicamento_ordenado_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
