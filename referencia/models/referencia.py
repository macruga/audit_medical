from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces
# importar los elementos de otros paquetes
from atencion_hc.models.atencion import atencionModel
from afiliados.models.afiliado import afiliadoModel
from afiliados.models.afiliacion import AfiliacionModel
from core.models.soporte.ips import IpsModel
from core.models.soporte.cups import CupsModel

from referencia.models.tipo_referencia import tipoReferenciaModel
from referencia.models.motivo_remision import motivoRemisionModel
from referencia.models.estado_referencia import estadoReferenciaModel
from referencia.models.motivo_decision import motivoDecisionModel

# Modelo de la Referencia y/o contrareferencia
class referenciaModel(models.Model):
    """
    Modelos de la clase de referencia
    
    Attributes
    ----------
    atencion_id: long
        Asociación a la atención que se relaciona con la referencia o contrareferencia
    paciente_id: long
        Asociación al paciente que se relaciona con la referencia o contrareferencia
    fecha: Date
        Fecha en al que se realiza la referencia o contrareferencia
    afiliacion_id: long
        Asociación a la afiliación del paciente con una EAPB
    servicio: string
        Campo de texto para la description del servicio
    viaje_ambulancia: boolean
        Indica sio la referencia se hace mediante viaje en ambulancia
    tipo_referencia_id: integer
        Indica si es referencia (0) o contrareferencia (1)
    motivo_remision_id: long
        Asociación con el motivo de remisión que causa la referencia o contrareferencia
    descripcion_remision: string
        Descricpción de la remisión
    nivel_de_atencion: int
        Nivel de la atención
    estado_id: integer
        Estado de la referencia o contrareferencia
    motivo_decision_id: integer
        Motivo para la decisión de la referencia o contrareferencia
    descripcion_decision: string
        Descricpción de la decisión
    tipo_formulario: string
        ???
    tipo_traslado: string
        ???
    fecha_radicacion: DateTime
        Fecha y hora de radicación de la referencia o contrareferencia
    ips_emisor_id: long
        Identificador de la IPS que refiere a un paciente
    ips_receptor_id: long
        Identificador de la IPS que recibe a un paciente referido
    codigo_cups_id: long
        Identificador del código CUPS relacionado con la referencia o contrareferencia
    traslado_prioridad: string
        Prioridad del traslado
    dias_tramite: integer
        Dias que dura el tramite de la referencia
    tiempo_gestion: integer
        Valor en minutos que duro la gestion de la referencia o contrareferencia 
    """
    
    atencion_id = models.ForeignKey(
        atencionModel,
        help_text="Atencion desde la que se hace la (Contra)Referencia",
        related_name="referencia_atencion",
        on_delete=models.PROTECT,
        db_column='atencion_id'
    )
    
    paciente_id = models.ForeignKey(
        afiliadoModel,
        help_text="Paciente que es referido",
        related_name="referencia_paciente",
        on_delete=models.PROTECT,
        db_column='paciente_id'
    )
    
    fecha = models.DateField(
        (), 
        help_text="Fecha de la referencia",
        auto_now=False, 
        auto_now_add=False, 
        null=True
    )
        
    afiliacion_id = models.ForeignKey(
        AfiliacionModel,
        help_text="Afiliación del paciente a una EAPB",
        related_name="referencia_afiliacion",
        on_delete=models.PROTECT,
        db_column='afiliacion_id'
    )
    
    viaje_ambulancia = models.BooleanField(
        help_text='Viaja en ambulancia'
    )
    
    tipo_referencia_id = models.ForeignKey(
        tipoReferenciaModel,
        help_text="tipo de referencia",
        related_name="referencia_tipo_referencia",
        on_delete=models.PROTECT,
        db_column='tipo_referencia_id'
    )
    
    motivo_remision_id = models.ForeignKey(
        motivoRemisionModel,
        help_text="Motivo de la referencia o contrareferencia",
        related_name="referencia_motivo_remision",
        on_delete=models.PROTECT,
        db_column='motivo_remision_id'
    )
    
    descripcion_remision = models.CharField(
        max_length=500,
        help_text='Descripción de la remisión',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
        
    nivel_de_atencion = models.IntegerField(
        help_text="Nivel de la atención",
        blank=False,
        null=False,
        validators = [onlyDigits]
    )
    
    estado_id = models.ForeignKey(
        estadoReferenciaModel,
        help_text="Estado de la referencia o contraeferencia",
        related_name="referencia_estado_referencia",
        on_delete=models.PROTECT,
        db_column='estado_id'
    )
    
    motivo_decision_id = models.ForeignKey(
        motivoDecisionModel,
        help_text="Motivo decisión de la referencia o contrareferencia",
        related_name="referencia_motivo_decision",
        on_delete=models.PROTECT,
        db_column='motivo_decision_id'
    )
    
    descripcion_decision = models.CharField(
        max_length=500,
        help_text='Descripción de la decisión',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
    
    tipo_formulario = models.CharField(
        max_length=50,
        help_text='Tipo de formulario de referencia o contrareferencia',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
    
    tipo_traslado = models.CharField(
        max_length=50,
        help_text='Tipo de traslado',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
    
    fecha_radicacion = models.DateTimeField(
        (),
        help_text="Fecha de radicación",
        auto_now=False, 
        auto_now_add=False
    )
    
    ips_emisor_id = models.ForeignKey(
        IpsModel,
        help_text="ips que referencia al paciente",
        related_name="referencia_ips_emisor",
        on_delete=models.PROTECT,
        db_column='ips_emisor_id'
    )
    
    ips_receptor_id= models.ForeignKey(
        IpsModel,
        help_text="ips que recibe al paciente referenciado",
        related_name="referencia_ips_receptor",
        on_delete=models.PROTECT,
        db_column='ips_receptor_id'
    )
    
    codigo_cups_id = models.ForeignKey(
        CupsModel,
        help_text="Código CUPS de la referencia o contrareferencia",
        related_name="referencia_cups",
        on_delete=models.PROTECT,
        db_column='codigo_cups_id'
    )
    
    traslado_prioridad = models.CharField(
        max_length=15,
        help_text='prioridad del traslado',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
    
    dias_tramite = models.PositiveSmallIntegerField(
        help_text = "Dias que dura el tramite de referencia o contrareferencia",
        validators = [
            onlyDigits,
            ]
    )
    
    tiempo_gestion = models.PositiveSmallIntegerField(
        help_text = "Tiempo en minutos de la gestión de la referencia o contrareferencia",
        validators = [
            onlyDigits,
            ]
    )
    
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_referencia_contrareferencia', on_delete=models.PROTECT)
    created = models.DateField((), auto_now=False, auto_now_add=True)

    def __str__(self):
        return '{}'.format( self.id )
        
    class Meta:
        app_label = 'referencia'
