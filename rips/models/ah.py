# CONSTRUCCIÓN DE MODELOS PENDIENTE
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, onlyCharactersAndDigits, onlyCharacters, onlyDigits, facturaType
from rips.models.via_ingreso import ViaIngresoModel
from rips.models.causa_externa import CausaExternaModel
from core.models.soporte.cie10 import Cie10Model
from rips.models.estado_salida import EstadoSalidaModel
from core.models.soporte.ips import IpsModel
from core.models.soporte.tipo_documento import TipoDocumentoModel 

# Definicion del modelo para los los rips AH (Hospitalizaciones)
class AhModel(models.Model):
    numero_factura = models.CharField(
        max_length=30,
        help_text='Numero de la Factura',
        unique=False,
        null=False,
        validators=[
            facturaType
        ]
    )
    codigo_prestador = models.ForeignKey( IpsModel, help_text='Codigo habilitacion del prestador', related_name='codigo_prestador_ah', on_delete=models.CASCADE )    
    tipo_identificacion_usuario = models.ForeignKey( TipoDocumentoModel, related_name = "tipo_identificacion_ah", on_delete = models.PROTECT )
    numero_identifacion_usuario = models.CharField(
        max_length=16,
        help_text='Numero de identificación del usuario',
        unique=False,
        null=False,
        blank=False,
        validators=[
            onlyCharactersAndDigits
        ]
    )   
    codigo_via_ingreso_institucion = models.ForeignKey(ViaIngresoModel, related_name='via_ingreso_hospitalizacion', on_delete=models.PROTECT)
    fecha_ingreso_usuario = models.DateField(('Fecha de ingreso del usuario a la instituciónn'), auto_now=False, auto_now_add=False)
    hora_ingreso_usuario = models.TimeField(('Hora de ingreso del usuario a la institucion'),)
    numero_autorizacion = models.CharField(
        max_length=20,
        help_text= 'Número de autorización',
        validators=[
            facturaType
        ]

    )
    codigo_causa_externa = models.ForeignKey(CausaExternaModel, related_name='causa_externa_hospitalizacion', on_delete=models.PROTECT)
    dx_principal_ingreso = models.ForeignKey(Cie10Model, related_name='diagnostico_principal_ingreso_hospitalizacion', on_delete=models.PROTECT)
    dx_principal_egreso = models.ForeignKey(Cie10Model, related_name='diagnostico_principal_egreso_hospitalizacion', on_delete=models.PROTECT)
    dx_relacionado1_egreso = models.ForeignKey(Cie10Model, related_name='diagnostico_relacionado1_egreso_hospitalizacion', on_delete=models.PROTECT)
    dx_relacionado2_egreso = models.ForeignKey(Cie10Model, related_name='diagnostico_relacionado2_egreso_hospitalizacion', on_delete=models.PROTECT)
    dx_relacionado3_egreso= models.ForeignKey(Cie10Model, related_name='diagnostico_relacionado3_egreso_hospitalizacion',  on_delete=models.PROTECT)                                                                            
    codigo_estado_salida = models.ForeignKey(EstadoSalidaModel, related_name='estado_salida_hospitalizacion', on_delete=models.PROTECT)
    dx_causa_muerte = models.ForeignKey(Cie10Model, related_name='causa_basica_muerte_hospitalizacion', on_delete=models.PROTECT) 
    fecha_salida_usuario = models.DateField(('Fecha de egreso del usuario a la institución'), auto_now=False, auto_now_add=False)
    hora_salida_usuario = models.TimeField(('Hora de egreso del usuario a la institución'),)

    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='user_create_ah', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.numero_identifacion_usuario)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_fac_ah_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_ah_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_ah_idx'),
            models.Index(fields=['fecha_ingreso_usuario'], name='fecha_ingreso_ah_idx'),
        ]
        
        constraints = [
            models.UniqueConstraint(fields=['numero_factura', 'numero_identifacion_usuario', 'fecha_ingreso_usuario' ], name='registro hospitalizacion unico')
        ] 
        app_label = 'rips'
