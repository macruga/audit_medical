from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces
#importar modelos de otros paquetes


from pqrs.models.tipo_pqrs import tipoPqrsModel
from pqrs.models.unidad_duracion import unidadDuracionModel

# Modelo de las PQRS Peticiones, Sugerencias, Quejas, Reclamos y Denuncias
class pqrsModel(models.Model):
    '''
    Modelo de la entidad que representa las PQRS.
    
    Attributes
    ----------
    codigo_radicacion: string
        Codigo asignado a la radicacion de la solicitud
    tipo_pqrs_id: long
        Relacion con el tipo de solicitud 
    description: string
        Texto que explica la solicitud
    area: string
        ???
    causal: string
        ???
    tecnologia: string
        ???
    observaciones: string
        Texto que contiene las observaciones de la solicitud
    observaciones_cierre: string 
        Texto que contiene las observaciones de cierre de la solicitud
    ultima_observacion: string
        última observación realizada en el proeso solicitado
    codigo: string
        ???
    fecha_recepcion: Date
        Fecha en la que se realizo la solicitud
    unidad_duracion_id: long
        Relacion con modelo de la unidad de duración
    duracion_gestion: integer
        Duración que tardo la gestion de la solicitud
    duracion_permitida: integer
        Diracion permitida de la gestion en la unidad de duración registrada
    
    tipo_de_poblacion???
    
    '''
    
    codigo_radicacion = models.CharField(
        max_length=30,
        help_text='Código de radicación de la solicitud',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
    
    tipo_pqrs_id = models.ForeignKey(
        tipoPqrsModel,
        help_text="Tipo de solicitud",
        related_name="pqrs_tipo_pqrs",
        on_delete=models.PROTECT,
        db_column='tipo_pqrs_id'
    )
    
    description = models.TextField(
        max_length=2000,
        help_text='Descripción de la solicitud',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
        ]
    )
    
    area = models.CharField(
        max_length=50,
        help_text='Área de la solicitud',
        unique=False,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
    
    causal = models.CharField(
        max_length=50,
        help_text='Causal de la solicitud',
        unique=False,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
    
    tecnologia = models.CharField(
        max_length=50,
        help_text='Tecnología de la solicitud',
        unique=False,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
    
    observaciones = models.TextField(
        max_length=500,
        help_text='Observaciones de la solicitud',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
        ]
    )
        
    observaciones_cierre = models.TextField(
        max_length=500,
        help_text='Observaciones de cierre de la solicitud',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
        ]
    )
        
    ultima_observacion = models.TextField(
        max_length=500,
        help_text='Última observacion realizada sobre el proceso de la solicitud',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
        ]
    )
    
    codigo = models.CharField(
        max_length=50,
        help_text='Código de la solicitud',
        unique=False,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    ) 
    
    fecha_recepcion = models.DateField(
        (),
        help_text="Fecha de recepción de la solicitud",
        auto_now=False, 
        auto_now_add=False
    )
    
    unidad_duracion_id = models.ForeignKey(
        unidadDuracionModel,
        help_text="Unidad de duración",
        related_name="pqrs_unidad_duracion",
        on_delete=models.PROTECT,
        db_column='unidad_duracion_id'
    )
    
    duracion_gestion = models.PositiveSmallIntegerField(
        help_text="Duración de la gestión de la solicitud"
    )
    
    duracion_permitida = models.PositiveSmallIntegerField(
        help_text="Duración permitida de la gestión de la solicitud"
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_pqrs', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo_radicacion )
    
    class Meta:
        app_label = 'pqrs'