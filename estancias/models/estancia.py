from django.db import models
from django.conf import settings
from datetime import date
from django.db.models import Q

# Validators
from django.core.validators import MaxValueValidator, MinValueValidator
from core.validators import currentDate

# Custome models
from afiliados.models.afiliado import afiliadoModel
from core.models.soporte.ips import IpsModel
from core.models.soporte.cie10 import Cie10Model
from censo.models.origen_evento import OrigenEventoModel
from censo.models.tipo_ingreso import TipoIngresoModel
from censo.models.condicion_alta import condicionAltaCensoModel
from censo.models.tipo_habitacion import TipoHabitacionModel


class EstanciaModel(models.Model): 
    '''
    Modelo de la relación (objeto) estancias del paciente, el estancias corresponde a la revista diaria de los
    medicos asores

    Attributes
    ----------
    id: int
        Número de identificador auto-incremental
    fecha_ingreso: Date
        Fecha de ingreso del paciente
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
    codigo_ips_id: str
        Vínculo con la relación de la IPS en donde se realiza el censo
    fecha_egreso: Date
        Fecha de egreso del paciente
    condicion_alta_id: int
        Vínculo con la relación de condición de alta para la salida del censo
    dx_egreso: int
        Vínculo de la relación con el CIE10 del diagnóstico de egreso del censo
    dias_estancia: int
        Campo numérico de los días de estancia del paciente en el censo
    reingreso: boolean
        Indicador de si el registro corresponde a un reingreso, por defecto False
    afiliado_id: int
        Identificador del paciente para la relación con la tabla de afiliados
    estado: boolean
        Indica el estado de la estancia, activa = True, inactiva = False
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

    dx_ingreso = models.ForeignKey(
        Cie10Model,
        related_name = "estancia_cie10_ingreso",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column="dx_ingreso"
    )

    tipo_ingreso_id = models.ForeignKey(
        TipoIngresoModel,
        related_name="estancia_tipo_ingreso",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="tipo_ingreso_id"
    )

    origen_evento_id = models.ForeignKey(
        OrigenEventoModel,
        related_name="estancia_origen_evento",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="origen_evento_id"
    )

    # TODO este diagnostico debe actualizarse automaticamente con la ultima evolucion 
    # y/o el registro del censo
    dx_actual = models.ForeignKey(
        Cie10Model,
        related_name = "estancia_cie10_actual",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column="dx_actual"
    )
    # TODO para el caso del prestador se debe tomar un valor default = al numero de habilitacion del prestador,
    #      para el caso de una aseguradora si debe indicar el codigo de habilitacion del prestador que atiende.
    codigo_ips_id = models.ForeignKey(
        IpsModel,
        related_name="estancia_ips",
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
        related_name="estancia_condicion_alta",
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        db_column="condicion_alta_id"
    )

    dx_egreso = models.ForeignKey(
        Cie10Model,
        related_name = "estancia_cie10_egreso",
        on_delete = models.PROTECT,
        null = True,
        blank = True,
        db_column="dx_egreso"
    )


    # campo calculado con script
    dias_estancia = models.PositiveIntegerField(
        help_text="Dias de estancia del paceinte en el censo",
        blank=True,
        default = 0,
        validators=[
            MaxValueValidator(1000), 
            MinValueValidator(1)
        ]
    )
    # TODO depende del servicio del ultimo egreso se marcar el reingreso, variable automatica
    #      Debe llevar mantenimiento para parametrizar los dias dependiendo del servicio
    reingreso = models.BooleanField(
        help_text="Indica si el registro es un reingreso",
        blank=False,
        null=False,
        default=False
    )

    afiliado_id = models.ForeignKey(
        afiliadoModel,
        related_name = "estancia_afiliado",
        on_delete=models.PROTECT,
        null=False,
        db_column="afiliado_id"
    ) 

    estado = models.BooleanField(default=True)
    usuario_egreso = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        related_name='user_egreso_estancia', 
        null=True,
        on_delete=models.PROTECT
        )
        
    fecha_registro_egreso = models.DateField(
        help_text="Fecha registro del egreso del paciente",
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        validators=[
            currentDate
        ]
    )

    dx_sindromatico = models.BooleanField(default=False)
    dx_alto_riesgo = models.BooleanField(default=False)
    estancia_prolongada = models.BooleanField(default=False)
    cohorte_seguimiento = models.BooleanField(default=False)
    

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_estancia', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )

    class Meta:
        app_label = 'estancias'
        constraints = [ # restriccion para que solo exista una estancia activa por usuario
            models.UniqueConstraint(fields=['afiliado_id', 'estado'], condition=Q(estado=True), name='Solo una estancia activa por usuario')
        ]