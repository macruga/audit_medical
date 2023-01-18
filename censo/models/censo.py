# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from core.validators import currentDate, noSpacesStartEnd, onlyCharactersAndDigits, onlyCharactersSpacesAndPunctuation

# importar los elementos de las otras bases de datos
from core.models.soporte.tipo_documento import TipoDocumentoModel
from core.models.soporte.cie10 import Cie10Model

from core.models.soporte.ips import IpsModel
from core.models.soporte.cie10 import Cie10Model
# from afiliados.models.afiliacion import AfiliacionModel
from afiliados.models.afiliado import afiliadoModel

# importar los elementos adicionales del paquete
from censo.models.tipo_ingreso import TipoIngresoModel
from censo.models.origen_evento import OrigenEventoModel
from censo.models.tipo_habitacion import TipoHabitacionModel
from censo.models.condicion_alta import condicionAltaCensoModel

# modelo de auditoria concurrente y retrospectiva
class censoModel (models.Model):
    '''
    Modelo de la relación (objeto) censo, el censo corresponde a la revista diaria de los 
    pacientes que están con una estancia activa de hoapitalización o que deben ser 
    contabilizados de acuerdo a su condición médica

    Attributes
    ----------
    id: int
        Número de identificador auto-incremental
    fecha_ingreso: Date
        Fecha de ingreso del paciente censado
    tipo_identificacion_id: int    
        Vínculo con la relación del tipo de identificación del paciente
    identificacion: str
        Identificación del paciente en el censo
    dx_ingreso: int
        Vínculo de la relación con el CIE10 del diagnóstico de ingreso
    tipo_ingreso_id: int
        Vínculo con la relación de tipo de ingreso al censo
    origen_evento_id: int
        Vínculo con la relación de origen del evento para censo
    dx_actual: int
        Vínculo de la relación con el CIE10 del diagnóstico actual del paciente censado
    tipo_habitacion_id: int
        Vínculo con la relación del tipo de servicio o habitación del censo
    codigo_ips_id: int
        Vínculo con la relación de la IPS en donde se realiza el censo
    fecha_egreso: Date
        Fecha de egreso del paciente
    condicion_alta_id: int
        Vínculo con la relación de condición de alta para la salida del censo
    dx_egreso: int
        Vínculo de la relación con el CIE10 del diagnóstico de egreso del censo
    fecha_censo: Date
        Fecha de recepcion de la información del censo del paciente
    responsable_carga_id: int
        Vínculo con la relación de los responsables para la carga del censo
    responsable_carga: str
        Identificación del responsable para la carga del censo
    dias_estancia: int
        Campo numérico de los días de estancia del paciente en el censo
    reingreso: boolean
        Indicador de si el registro corresponde a un reingreso, por defecto False
    afiliado_id: int
        Identificador del paciente para la relación con la tabla de afiliados
    afiliacion_id: int
        Identificador de la afiliacion del paciente, vínculo para la relación con la tabla de afiliacion
    nota: Str
        Nota de la carga del censo del paciente
    created: Date
        Fecha de carga del registro del censo en el sistema
    owner_id: int 
        Vínculo con la relación de los responsables para la carga del censo
    active: Boolean
        Indica si este registro esta activo o no
    
    '''
    fecha_ingreso = models.DateField(
        help_text="Fecha de ingreso del paciente",
        auto_now=False,
        auto_now_add=False,
        blank=False,
        null=False,
        validators=[
            currentDate
        ]
    )

    tipo_identificacion_id = models.ForeignKey(
        TipoDocumentoModel,
        related_name="censo_tipo_documento",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="tipo_identificacion_id"
    )

    identificacion = models.CharField(
        max_length=15,
        help_text='identificación del paceinte censado',
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )

    dx_ingreso = models.ForeignKey(
        Cie10Model,
        related_name = "censo_cie10_ingreso",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column="dx_ingreso"
    )

    tipo_ingreso_id = models.ForeignKey(
        TipoIngresoModel,
        related_name="censo_tipo_ingreso",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="tipo_ingreso_id"
    )

    origen_evento_id = models.ForeignKey(
        OrigenEventoModel,
        related_name="censo_origen_evento",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="origen_evento_id"
    )

    dx_actual = models.ForeignKey(
        Cie10Model,
        related_name = "censo_cie10_actual",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column="dx_actual"
    )
    
    tipo_habitacion_id = models.ForeignKey(
        TipoHabitacionModel,
        related_name="censo_tipo_habitacion",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="tipo_habitacion_id"
    )

    codigo_ips_id = models.ForeignKey(
        IpsModel,
        related_name="censo_ips",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="codigo_ips_id"
    )

    fecha_egreso = models.DateField(
        help_text="Fecha de egreso del paciente",
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        validators=[
            currentDate
        ]
    )

    condicion_alta_id = models.ForeignKey(
        condicionAltaCensoModel,
        related_name="censo_condicion_alta",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column="condicion_alta_id"
    )

    dx_egreso = models.ForeignKey(
        Cie10Model,
        related_name = "censo_cie10_egreso",
        on_delete = models.PROTECT,
        null = True,
        blank = True,
        db_column="dx_egreso"
    )

    # fecha_recepcion = models.DateField(
    fecha_censo = models.DateField(
        help_text="Fecha de recepción del censo del paciente",
        auto_now=False,
        auto_now_add=False,
        blank=False,
        null=False,
        validators=[
            currentDate
        ]
    )

    # campos calculados ???
    dias_estancia = models.PositiveIntegerField(
        help_text="Dias de estancia del paceinte en el censo",
        blank=True,
        validators=[
            MaxValueValidator(1000), 
            MinValueValidator(1)
        ]
    )

    reingreso = models.BooleanField(
        help_text="Indica si el registro es un reingreso",
        blank=False,
        null=False,
        default=False
    )

    # Campos Extra 
    afiliado_id = models.ForeignKey(
        afiliadoModel,
        related_name = "censo_afiliado",
        on_delete=models.PROTECT,
        null=False,
        db_column="afiliado_id"
    )

    # afiliacion_id = models.ForeignKey(
    #     AfiliacionModel,
    #     related_name="censo_afiliacion",
    #     on_delete=models.PROTECT,
    #     null=False,
    #     db_column="afiliacion_id"
    # )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_censo', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
    
    class Meta:
        app_label = 'censo'
        # Add some validations here