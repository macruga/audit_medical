# ## ### ##### ####### ########### ############# ################# ################## 

from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces
#importar modelos de otros paquetes
from afiliados.models.afiliado import afiliadoModel
from core.models.soporte.tipo_documento import TipoDocumentoModel
from afiliados.models.afiliacion import AfiliacionModel
from core.models.soporte.aseguradoras import aseguradorasModel
from contratacion.models.contratacion import contratacionModel

from autorizaciones.models.estado_autorizacion import estadoAutorizacionModel
from autorizaciones.models.codigo_clasificacion_triage import codigoClasificacionTriageModel
from autorizaciones.models.plan_servicio import planServicioModel


# Modelo de la Autorizacion
class autorizacionModel(models.Model):
    '''
    Modelo de la entidad autorización base de las autorizaciones.
    
    Attributes
    ----------
    numero_autorizacion: string
        Número de referencia de la autorizacion
    fecha_solicitud: DateTime
        Fecha y hora de la solicitud de autorizacion
    fecha_respuesta: DateTime
        Fecha y hora de la respuesta a la solicitud de autorizacion
    afiliado_id: long
        Relación con la tabla de afiliado
    tipo_identificacion_id: string
        Relacion con el tipo de documento del afiliado
    identificaion: string
        La identificación del paciente
    afiliacion_id: long
        Relacion con la afiliación activa del paciente
    eapb_id: long
        Relacion con la aseguradora a quien se solicita la autorización
    contrato_id: long
        Relación con el contrato del que hace parte la autorización
    estado_solicitud_id: long
        Relación con la tabla de estados de solicitudes de autorización
    descipcion_servicio: string
        Descripcion del servicio a autorizar
    plan_servicio_id: long
        Relación al plan de servicio autorizado (RC, RS, MP, PC)
    codigo_clasificacion_triage_id: long
        Relacion con la tabla de codigos de clasificación del triage
    descripcion_clasificacion_triage: string
        Descripción de la clasificacion del paciente en el triage
    '''
    
    numero_autorizacion = models.CharField(
        max_length=30,
        help_text='Número de la autorizacion',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    
    fecha_solicitud = models.DateTimeField(
        (),
        help_text="Fecha de solicitud",
        auto_now=False, 
        auto_now_add=False
    )
    
    fecha_respuesta = models.DateTimeField(
        (),
        help_text="Fecha de respuesta a la solicitud",
        auto_now=False, 
        auto_now_add=False
    )
    
    afiliado_id = models.ForeignKey(
        afiliadoModel,
        help_text="Paciente que esta tramitando la autorización",
        related_name="autorizacion_paciente",
        on_delete=models.PROTECT,
        db_column='paciente_id'
    )
    
    tipo_identificacion_id = models.ForeignKey(
        TipoDocumentoModel, 
        related_name='autorizacion_tipo_identificacion',
        on_delete=models.PROTECT,
        unique=False,
        null=False,
        help_text='Tipo de identificación del paciente',
        db_column="tipo_identificacion_id"
    )
    
    identificacion = models.CharField(
        max_length=100,
        help_text='Identificacion del afiliado',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]       
    )

    afiliacion_id = models.ForeignKey(
        AfiliacionModel,
        help_text="Afiliación del paciente a una EAPB",
        related_name="autorizacion_afiliacion",
        on_delete=models.PROTECT,
        db_column='afiliacion_id',
        null=True,
    )

    eapb_id = models.ForeignKey(
        aseguradorasModel,
        help_text="EAPB para la autorización",
        related_name="autorizacion_aseguradora",
        on_delete=models.PROTECT,
        db_column='eapb_id'
    )
    
    contrato_id = models.ForeignKey(
        contratacionModel,
        help_text='Contrato de la autorización',
        related_name='autorizacion_contratacion',
        on_delete=models.PROTECT,
        null=True,
        db_column='contrato_id'
    )

    estado_solicitud_id = models.ForeignKey(
        estadoAutorizacionModel,
        help_text="Estado de la solicitud de autorización",
        related_name="autorizacion_estado_autorizacion",
        on_delete=models.PROTECT,
        db_column='estado_solicitud_id'
    )

    descripcion_servicio = models.CharField(
        max_length=250,
        help_text='Descripción del servicio a autorizar',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    plan_servicio_id = models.ForeignKey(
        planServicioModel,
        help_text="Plan de servicios e la autorización",
        related_name="autorizacion_objeto_plan_servicios",
        on_delete=models.PROTECT,
        db_column='plan_servicio_id'
    )


    codigo_clasificacion_triage_id = models.ForeignKey(
        codigoClasificacionTriageModel,
        help_text="Código de clasificación de triage de autorización de Urgencias",
        related_name="autorizacion_codigo_clasificacion_triage",
        on_delete=models.PROTECT,
        db_column='codigo_clasificacion_triage_id',
        null=True
    )

    descripcion_clasificacion_triage = models.CharField(
        max_length=250,
        help_text='Descripción de clasificación de triage de autorización de Urgencias',
        unique=False,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    
    created = models.DateField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_autorizacion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.numero_autorizacion )
        
    class Meta:
        app_label = 'autorizaciones'