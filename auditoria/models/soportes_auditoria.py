# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharacters, onlyAlphaNumeric, onlyCharactersAndSpaces, onlyCharactersSpacesAndPunctuation, onlyCharactersAndDigits, onlyDigits, onlyDigitsAndPoints, currentDate, rangeDate, facturaType

# importar los elementos de las otras bases de datos

# importar los elementos adicionales del paquete
from auditoria.models.tipo_soporte import tiposSoporteModel
from auditoria.models.auditoria import auditoriaModel

# modelo de Fugas para la Auditoria
class soportesAuditoriaModel (models.Model):
    '''
    Modelo de la relación soportes de auditoría

    Attributes
    ----------
    tipo_soporte_id: int
        Relación con el tipo de soporte
    fecha_inicio: Date
        Fecha de inicio del soporte
    fecha_fin: Date
        Fecha de fin del soporte
    '''
    tipo_soporte_id = models.ForeignKey(
        tiposSoporteModel,
        related_name = "soporte_tipo_soporte",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column = "tipo_soporte_id"
    )
    auditoria_id = models.ForeignKey(
        auditoriaModel,
        related_name = "soporte_auditoria",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column = "auditoria_id"
    )
    fecha_inicio = models.DateField(
        (), 
        auto_now=False, 
        auto_now_add=False, 
        help_text="Fecha de inicio",
        blank=False, 
        null=False, 
        validators=[currentDate]
    )
    fecha_fin = models.DateField(
        (), 
        auto_now=False, 
        auto_now_add=False, 
        help_text="Fecha de fin",
        blank=True, 
        null=True, 
        validators=[currentDate]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_soporte_auditoria', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'auditoria'

