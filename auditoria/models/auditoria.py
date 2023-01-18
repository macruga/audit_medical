# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings
# from django.db.models.deletion import PROTECT
from django.core.validators import MaxValueValidator, MinValueValidator

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharacters, onlyAlphaNumeric, onlyCharactersAndSpaces, onlyCharactersSpacesAndPunctuation, onlyCharactersAndDigits, onlyDigits, onlyDigitsAndPoints, currentDate, rangeDate, facturaType
# importar los elementos de las otras bases de datos
from censo.models.censo import censoModel
from core.models.soporte.cie10 import Cie10Model


from core.models.soporte.aseguradoras import aseguradorasModel
from core.models.soporte.ips import IpsModel
from afiliados.models.afiliado import afiliadoModel
from afiliados.models.afiliacion import afiliacionModel

# importar los elementos adicionales del paquete
from auditoria.models.auditor import auditorModel
from auditoria.models.tipo_contratos import tiposContratoModel


# modelo de auditoria concurrente y retrospectiva
class auditoriaModel (models.Model):
    '''
    Modelo de la relación (objeto) Auditoria, la auditoria se realiza sobre una atención
    ???

    Attributes
    ----------
    auditoria_id: long
        Número secuencial que identifica un registro de auditoría
    censo_id: long
        Relación con el censo que debe ser auditado en concurrencia
    dignostico_id: long
        Relación con el cie10 del diagnostico principal
    dignostico_uno_id: long
        Relación con el cie10 del diagnostico asociado
    dignostico_dos_id: long
        Relación con el cie10 del diagnostico dos
    fecha_concurrencia: Date
        Fecha en que se realizó la auditoria concurrente
    
    tipo_contrato_id: long
        Relación con el tipo de contrato 
    recobro_id: long
        Relación con el tipo de recobro relacionado al contrato 
    consulta_hc_amb:  Date
        Fecha de la última consulta ambulatoria del paciente
    orden_reingreso_id: long
        Relación con el tipo de orden de reingreso 
    edad_gestacional: int
        Edad gestacional, cantidad de semanas solo para diagnostico proncipal gestante
    fecha_ultima_regla: Date
        Fecha de al ultima regla
    edad_neonato: Date
        Fecha de nacimiento del neonato
    peso_neonato: int
        Peso del neonato (en gramos)
    edad_corregida: bool
        Si se corrigió la fecha de nacimiento del neonato
    peso_corregido: bool
        Si se corrigió el peso del neonato
    '''
    auditoria_id = models.PositiveBigIntegerField(
        help_text="Número secuencial que identifica un registro de auditoría",
        unique=True,
        blank=False,
        db_column="auditoria_id"
    )
    censo_id = models.ForeignKey(
        censoModel,
        related_name="auditoria_censo",
        on_delete=models.PROTECT,
        null=False,
        db_column="censo_id"
    )
    dignostico_id = models.ForeignKey(
        Cie10Model,
        related_name="auditoria_dx_cie10",
        on_delete=models.PROTECT,
        null=False,
        db_column="dignostico_id"
    )
    dignostico_uno_id = models.ForeignKey(
        Cie10Model,
        related_name="auditoria_dx_uno_cie10",
        on_delete=models.PROTECT,
        null=True,
        db_column="dignostico_uno_id"
    )
    dignostico_dos_id = models.ForeignKey(
        Cie10Model,
        related_name="auditoria_dx_dos_cie10",
        on_delete=models.PROTECT,
        null=True,
        db_column="dignostico_dos_id"
    )
    fecha_concurrencia = models.DateField(
        (), 
        auto_now=False, 
        auto_now_add=False, 
        help_text="Fecha de la auditoria concurrente",
        blank=False, 
        null=False, 
        validators=[currentDate]
    )
    evolucion = models.TextField(
        max_length=4000,
        help_text="Historia clínica del día",
        null=False,
        blank=False,
        validators=[onlyCharactersSpacesAndPunctuation]
    )
    tipo_contrato_id = models.ForeignKey(
        tiposContratoModel,        
        related_name = "auditoria_tipo_contrato",
        on_delete = models.PROTECT,
        db_column = "tipo_contrato_id"
    )
    recobro_id  = models.ForeignKey(
################################## Falta la relacion        
        related_name = "auditoria_recobro",
        on_delete = models.PROTECT,
        db_column = "recobro_id"
    )
    consulta_hc_amb = models.DateField(
        (), 
        auto_now=False, 
        auto_now_add=False, 
        help_text="Fecha de la última consulta ambulatoria",
        blank=True, 
        null=True, 
        validators=[currentDate]
    )
    orden_reingreso_id = models.ForeignKey(
################################## Falta la relacion        
        related_name = "auditoria_orden_reingreso",
        on_delete = models.PROTECT,
        db_column = "orden_reingreso_id"
    )
    edad_gestacional = models.PositiveIntegerField(
        help_text="Edad gestacional",
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(50), 
            MinValueValidator(0)
        ]
    )
    fecha_ultima_regla = models.DateField(
        (), 
        auto_now=False, 
        auto_now_add=False, 
        help_text="Fecha de la última regla",
        blank=True, 
        null=True, 
        validators=[currentDate]
    )
    edad_neonato = models.DateField(
        (), 
        auto_now=False, 
        auto_now_add=False, 
        help_text="Fecha de nacimiento del neonato",
        blank=True, 
        null=True, 
        validators=[currentDate]
    )
    peso_neonato = models.PositiveIntegerField(
        help_text="Peso del neonato",
        blank=True,
        null=True,
        validators=[
            MaxValueValidator(10000), 
            MinValueValidator(0)
        ]
    )
    edad_corregida = models.BooleanField(
        help_text="Fecha de naciemiento de neonato corregida",
        default=False
    )
    peso_corregido = models.BooleanField(
        help_text="Peso del neonato corregida",
        default=False
    )
    observacion_egreso = models.TextField(
        max_length=2000,
        help_text="Nota de concurrencia del auditor en al auditoría",
        null=False,
        blank=False,
        validators=[onlyCharactersSpacesAndPunctuation]
    )
    


    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_auditoria', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
    
    # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
    class Meta:
        app_label = 'auditoria'