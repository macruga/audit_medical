# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharacters, onlyAlphaNumeric, onlyCharactersAndSpaces, onlyCharactersSpacesAndPunctuation, onlyCharactersAndDigits, onlyDigits, onlyDigitsAndPoints, currentDate, rangeDate, facturaType
# importar los elementos de las otras bases de datos
from core.models.soporte.cums import CumsModel
from core.models.soporte.cups import CupsModel

# importar los elementos adicionales del paquete
from auditoria.models.tipo_fugas import tiposFugaModel

from auditoria.models.auditoria import auditoriaModel

# modelo de Fugas para la Auditoria
class fugasAuditoriaModel (models.Model):
    '''
    Modelo de la relación Fugas auditoría

    Attributes
    ----------
    tipo_fuga_id: int
        Relación con el tipo de fuga
    fecha_solicitud: Date
        Fecha de la solicitud de la fuga
    fecha_radicacion_eps: Date
        Fecha de la radicación de la fuga en la eps
    codigo_cups_fuga_id: int
        relación con el código cups de la fuga (puede ser vacio si hay codigo cums)
    codigo_cums_fuga_id: int
        relación con el código cups de la fuga (puede ser vacio si hay codigo cups)


    description: str
        La fuga en el procedimiento para la auditoría
    '''
    tipo_fuga_id = models.ForeignKey(
        tiposFugaModel,
        related_name="fuga_tipo_fuga",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="tipo_fuga_id"
    )

    auditoria_id = models.ForeignKey(
        auditoriaModel,
        related_name="fuga_auditoria",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="auditoria_id"
    )

    fecha_solicitud = models.DateField(
        (), 
        auto_now=False, 
        auto_now_add=False, 
        help_text="Fecha de la solicitud",
        blank=False, 
        null=False, 
        validators=[currentDate])

    fecha_radicacion_eps = models.DateField(
        (), 
        auto_now=False, 
        auto_now_add=False, 
        help_text="Fecha de la radicación a la eps",
        blank=True, 
        null=True, 
        validators=[currentDate])

    codigo_cups_fuga_id = models.ForeignKey(
        CupsModel,
        related_name="fuga_cups",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column="codigo_cups_fuga_id"
    )

    codigo_cums_fuga_id = models.ForeignKey(
        CumsModel,
        related_name="fuga_cums",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column="codigo_cums_fuga_id"
    ) 

    fecha_prestacion = models.DateField(
        (), 
        auto_now=False, 
        auto_now_add=False, 
        help_text="Fecha de la prestación",
        validators=[currentDate])

    fecha_autorizacion = models.DateField(
        (), 
        auto_now=False, 
        auto_now_add=False, 
        help_text="Fecha de la autorizacion",
        validators=[currentDate])
    
    dias_fuga = models.PositiveIntegerField(
        help_text="Días de fuga",
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(1000), 
            MinValueValidator(1)
        ]
    )

    valor_fuga = models.DecimalField(
        help_text = "Valor de la fuga",
        blank = True,
        null = True,
        # validators = [ ]
    ) 

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_fuga_auditoria', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'auditoria'

