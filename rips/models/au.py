# CONSTRUCCIÓN DE MODELOS PENDIENTE
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, onlyCharactersAndDigits, onlyCharacters, onlyDigits, facturaType
from rips.models.causa_externa import CausaExternaModel
from core.models.soporte.cie10 import Cie10Model
from rips.models.destino_salida_obs import DestionSalidaObsModel
from rips.models.estado_salida import EstadoSalidaModel
from core.models.soporte.ips import IpsModel
from core.models.soporte.tipo_documento import TipoDocumentoModel 

# Definicion del modelo para los los rips AU (Urgencias)
class AuModel(models.Model):
    numero_factura = models.CharField(
        max_length=30,
        help_text='Numero de la Factura',
        unique=False,
        null=False,
        validators=[
            facturaType
        ]
    )
    codigo_prestador = models.ForeignKey( IpsModel, help_text='Codigo habilitacion del prestador', related_name='codigo_prestador_au', on_delete=models.CASCADE )
    tipo_identificacion_usuario = models.ForeignKey( TipoDocumentoModel, related_name = "tipo_identificacion_au", on_delete = models.PROTECT )
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
    fecha_ingreso_usuario = models.DateField(('Fecha de ingreso del usuario a observación'), auto_now=False, auto_now_add=False)
    hora_ingreso_usuario = models.TimeField(('Hora de ingreso del usuario a observación'),)
    numero_autorizacion = models.CharField(
        max_length=20,
        help_text= 'Número de autorización',
        validators=[
            facturaType
        ]

    )
    codigo_causa_externa = models.ForeignKey(CausaExternaModel, related_name='causa_externa_urgencias', on_delete=models.PROTECT)
    dx_salida = models.ForeignKey(Cie10Model, related_name='diagnostico_salida_urgencias', on_delete=models.PROTECT)
    dx_relacionado1_salida = models.ForeignKey(Cie10Model, related_name='diagnostico_relacionado1_salida_urgencias', on_delete=models.PROTECT)
    dx_relacionado2_salida = models.ForeignKey(Cie10Model, related_name='diagnostico_relacionado2_salida_urgencias', on_delete=models.PROTECT)
    dx_relacionado3_salida = models.ForeignKey(Cie10Model, related_name='diagnostico_relacionado3_salida_urgencias', on_delete=models.PROTECT)                                                                            
    codigo_destino_salida_usuario = models.ForeignKey(DestionSalidaObsModel, related_name='destino_salida_urgencias', on_delete=models.PROTECT) 
    codigo_estado_salida = models.ForeignKey(EstadoSalidaModel, related_name='estado_salida_urgencias', on_delete=models.PROTECT)
    causa_basica_muerte = models.ForeignKey(Cie10Model, related_name='causa_basica_muerte_urgencias', on_delete=models.PROTECT) 
    fecha_salida_usuario = models.DateField(('Fecha de salida del usuario a observación'), auto_now=False, auto_now_add=False)
    hora_salida_usuario = models.TimeField(('Hora de salida del usuario a observación'),)

    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='user_create_affiles', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.numero_identifacion_usuario)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_fac_au_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_au_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_au_idx'),
            models.Index(fields=['fecha_ingreso_usuario'], name='fecha_ingreso_au_idx'),
        ]
        # Solo pude existir un numero de factura asociado a un prestador
        constraints = [
            models.UniqueConstraint(fields=['numero_factura', 'numero_identifacion_usuario', 'fecha_ingreso_usuario' ], name='registro urgencias unico')
        ] 
        app_label = 'rips'
