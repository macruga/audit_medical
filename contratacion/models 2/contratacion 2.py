from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces, onlyDigitsAndPoints
#importar modelos de otros paquetes
from core.models.soporte.ips import IpsModel

from contratacion.models.tarifario_contratado import tarifarioContratadoModel
from contratacion.models.estado_contrato import estadoContratoModel

# Modelo de la contratacion
class contratacionModel(models.Model):
    '''
    Modelo de la entidad contratacion.
    
    Attributes
    ----------
    ips_id: long
        Relacion con el modelo de IPS
    codigo_servicio: string
        Código del servicio contratado
    *tarifario_contratado_id: long
        Relacion con el tipo de tarifario contratado
    *porcentaje: double
        Procentaje del contrato
    fecha_inicio: Date
        Fecha de inicio de la contratación
    fecha_fin: Date
        Fecha de finalización de la contratación
    estado_contrato_id: string
        Estado del contrato
    contratado: boolean
        True si esta contratado o False en caso contrario
    
    
    autorizacion: string
        Número asociado al registro en autorizaciones
    
    '''
    
    ips_id = models.ForeignKey(
        IpsModel,
        help_text="ips de la contratacion",
        related_name="contratacion_ips",
        on_delete=models.PROTECT,
        db_column='ips_id'
    )
    
    codigo_servicio = models.CharField(
        max_length=50,
        help_text='Código del servicio contratado',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
    
    tarifario_contratado_id = models.ForeignKey(
        tarifarioContratadoModel,
        help_text="Tipo de tarifario contratado",
        related_name="contratacion_tarifario_contratado",
        on_delete=models.PROTECT,
        db_column='tarifario_contratado_id'
    )
    
    porcentaje = models.DecimalField(
        help_text='Porcentaje del contrato, valor entre 0 y 100 con un digito decimal',
        max_digits=5,
        decimal_places=1,
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyDigitsAndPoints,
        ]
    )
        
    fecha_inicio = models.DateField(
        (),
        help_text="Fecha de inicio de la contratación",
        auto_now=False, 
        auto_now_add=False
    )
    
    fecha_fin = models.DateField(
        (),
        help_text="Fecha de finalización de la contratación",
        auto_now=False, 
        auto_now_add=False
    )
    
    estado_contrato_id = models.ForeignKey(
        estadoContratoModel,
        help_text="Estado del contrato",
        related_name="contratacion_estado_contrato",
        on_delete=models.PROTECT,
        db_column='estado_contrato_id'
    )
    
    contratado = models.BooleanField(
        help_text='Si o No'
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_contratacion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
    
    class Meta:
        app_label = 'contratacion'