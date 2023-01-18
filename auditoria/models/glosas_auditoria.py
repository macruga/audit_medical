# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharacters, onlyAlphaNumeric, onlyCharactersAndSpaces, onlyCharactersSpacesAndPunctuation, onlyCharactersAndDigits, onlyDigits, onlyDigitsAndPoints, currentDate, rangeDate, facturaType
# importar los elementos de las otras bases de datos
from core.models.soporte.cums import CumsModel
from core.models.soporte.cups import CupsModel

# importar los elementos adicinales del paquete
from auditoria.models.tipo_glosa import tipoGlosaAuditoriaModel
from auditoria.models.auditoria import auditoriaModel


# modelo de Auditor que realiza una auditoría
class glosasAuditoriaModel (models.Model):
    """
    Modelo de la relación (objeto) glosasAuditoria, que representa el ejercicio de una glosa realizada por un auditor

    Attributes
    ----------
    tipo_glosa_id: long
        Relación con el modelo de tipos de glosa
    auditoria_id: long
        Relación con el modelo auditoria, a la auditoría realizada por el auditor
    codigo_cums_glosa_id: int
        relación con el código cums de la fuga (puede ser vacio si hay codigo cups)
    codigo_cups_glosa_id: int
        relación con el código cups de la fuga (puede ser vacio si hay codigo cums)
    observacion_glosa: str
        Texto con la observación de la glosa hecha por el auditor
    valor_glosa: double
        Valor estimado de la glosa
    cantidad_glosada:int
        Cantidad del elemento glosado
    """
    tipo_glosa_id = models.ForeignKey(
        tipoGlosaAuditoriaModel,
        related_name = "auditoria_tipo_glosa",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column = "tipo_glosa_id"
    )
    auditoria_id = models.ForeignKey(
        auditoriaModel,
        related_name = "glosa_auditoria",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column = "auditoria_id"
    )
    codigo_cups_glosa_id = models.ForeignKey(
        CupsModel,
        related_name="glosa_cups",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column="codigo_cups_glosa_id"
    )
    codigo_cums_glosa_id = models.ForeignKey(
        CumsModel,
        related_name="glosa_cums",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column="codigo_cums_glosa_id"
    ) 
    observacion_glosa = models.TextField(
        max_length=1500,
        help_text="observación de la glosa",
        null=False,
        blank=False,
        validators=[ ]
    )
    valor_glosa = models.DecimalField(
        help_text="Valor de la glosa",
        blank=True,
        null=True,
        validators = []
    )
    cantidad_glosada = models.PositiveIntegerField(
        help_text="Cantidad glosada",
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(1000), 
            MinValueValidator(0)
        ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_glosa_auditoria', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
    
    class Meta:
        app_label = 'auditoria'
        