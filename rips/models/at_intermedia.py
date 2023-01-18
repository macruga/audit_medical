# CONSTRUCCIÓN DE MODELOS PENDIENTE
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, onlyCharactersAndDigits, onlyCharacters, onlyDigits, facturaType

# Definicion del modelo para los los rips AT (Otros servicios)
class AtIntermediaModel(models.Model):
    numero_factura = models.CharField(
        max_length=40,
        help_text='Numero de la Factura',
        unique=False,
        null=True,
    )
    
    codigo_prestador = models.CharField(
        max_length=20,
        help_text='Codigo del prestador',
        unique=False,
        null=True,
    )
    tipo_identificacion_usuario = models.CharField(
        max_length=10,
        help_text='Tipo de identificacion',
        unique=False,
        null=True,
    )
    numero_identifacion_usuario = models.CharField(
        max_length=20,
        help_text='Numero de identificación del usuario',
        unique=False,
        null=True
    )
    numero_autorizacion = models.CharField(
        max_length=20,
        help_text= 'Número de autorización', 
        unique=False,
        null=True
    )
    codigo_tipo_servicio = models.CharField(
        max_length=20,
        help_text= 'Codigo tipo del servicio', 
        unique=False,
        null=True
    )
    codigo_servicio = models.CharField(
        max_length=20,
        help_text= 'Código del servicio',
        unique=False,
        null=True,
    )
    nombre_servicio = models.CharField(
        max_length=200,
        help_text= 'Nombre del servicio',
        unique=False,
        null=True,
    )

    cantidad = models.DecimalField(
        help_text='Cantidad',
        max_digits=20,
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
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='user_create_at_int', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return '{}'.format(self.id)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_fac_at_int_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_at_int_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_at_int_idx'),
            models.Index(fields=['codigo_servicio'], name='codigo_servicio_at_int_idx'),
            models.Index(fields=['nombre_servicio'], name='nombre_servicio_at_int_idx'),
        ]
        
        constraints = [
            models.UniqueConstraint(fields=[
                'numero_factura', 
                'codigo_prestador',
                'numero_identifacion_usuario', 
                'tipo_identificacion_usuario', 
                'codigo_tipo_servicio',
                'codigo_servicio',
                'nombre_servicio',
                'cantidad',
                'valor_unitario',
                'valor_total'
                ], name='registro at_int unico')
        ] 
        app_label = 'rips'
