# CONSTRUCCIÓN DE MODELOS PENDIENTE
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, onlyCharactersAndDigits, onlyCharacters, onlyDigits, facturaType, onlyCharactersSpacesAndPunctuation
from rips.models.tipo_servicio import TipoServicioModel
from core.models.soporte.ips import IpsModel
from core.models.soporte.tipo_documento import TipoDocumentoModel 

# Definicion del modelo para los los rips AT (Otros servicios)
class AtModel(models.Model):
    numero_factura = models.CharField(
        max_length=30,
        help_text='Numero de la Factura',
        unique=False,
        null=False,
        validators=[
            facturaType
        ]
    )
    codigo_prestador = models.ForeignKey( IpsModel, help_text='Codigo habilitacion del prestador', related_name='codigo_prestador_at', on_delete=models.CASCADE )    
    tipo_identificacion_usuario = models.ForeignKey( TipoDocumentoModel, related_name = "tipo_identificacion_at", on_delete = models.PROTECT )
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
    numero_autorizacion = models.CharField(
        max_length=20,
        help_text= 'Número de autorización',
        validators=[
            facturaType
        ]

    )
    codigo_tipo_servicio = models.ForeignKey(TipoServicioModel, related_name='tipo_servicio_otros_servicios', on_delete=models.PROTECT)
    codigo_servicio = models.CharField(
        max_length=20,
        help_text= 'Código del servicio',
        unique=False,
        null=True,
        validators=[
            onlyCharactersAndDigits
        ]
    )
    nombre_servicio = models.CharField(
        max_length=150,
        help_text= 'Nombre del servicio',
        unique=False,
        null=False,
        validators=[
            onlyCharactersSpacesAndPunctuation
        ]
    )

    cantidad = models.DecimalField(
        help_text='Cantidad',
        max_digits=10,
        decimal_places=1,
        default=0.0
    )

    valor_unitario = models.DecimalField(
        help_text='Valor unitario',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    valor_total = models.DecimalField(
        help_text='Valor total',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )

    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='user_create_at', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return '{}'.format(self.id)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_fac_at_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_at_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_at_idx'),
            models.Index(fields=['nombre_servicio'], name='nombre_servicio_at_idx'),
        ]
        
        constraints = [
            models.UniqueConstraint(fields=['numero_factura', 'numero_identifacion_usuario', 'nombre_servicio' ], name='registro at unico')
        ] 
        app_label = 'rips'
