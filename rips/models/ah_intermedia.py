# CONSTRUCCIÓN DE MODELOS PENDIENTE
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, onlyCharactersAndDigits, onlyCharacters, onlyDigits, facturaType

# Definicion del modelo para los los rips AH (Hospitalizaciones)
class AhIntermediaModel(models.Model):
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
    codigo_via_ingreso_institucion = models.CharField(
        max_length=10,
        help_text= 'Codigo via de ingreso', 
        unique=False,
        null=True
    )
    fecha_ingreso_usuario = models.CharField(
        max_length=22,
        help_text='Fecha Ingreso',
        unique=False,
        null=True,
    )
    hora_ingreso_usuario = models.CharField(
        max_length=22,
        help_text='Hora ingreso',
        unique=False,
        null=True,
    )
    numero_autorizacion = models.CharField(
        max_length=30,
        help_text= 'Número de autorización', 
        unique=False,
        null=True
    )
    codigo_causa_externa = codigo_causa_externa = models.CharField(
        max_length=20,
        help_text= 'Codigo causa externa', 
        unique=False,
        null=True
    )
    dx_principal_ingreso = models.CharField(
        max_length=20,
        help_text= 'Diagnostico principal de ingreso', 
        unique=False,
        null=True
    )
    dx_principal_egreso = models.CharField(
        max_length=20,
        help_text= 'Diagnostico principal de egreso', 
        unique=False,
        null=True
    )
    dx_relacionado1_egreso = models.CharField(
        max_length=20,
        help_text= 'Diagnostico relacionado 1 de egreso', 
        unique=False,
        null=True
    )
    dx_relacionado2_egreso = models.CharField(
        max_length=20,
        help_text= 'Diagnostico relacionado 2 de egreso', 
        unique=False,
        null=True
    )
    dx_relacionado3_egreso = models.CharField(
        max_length=20,
        help_text= 'Diagnostico relacionado 3 de egreso', 
        unique=False,
        null=True
    )  
    dx_complicacion= models.CharField(
        max_length=20,
        help_text= 'Diagnostico complicacion', 
        unique=False,
        null=True
    )                                                                          
    codigo_estado_salida = models.CharField(
        max_length=20,
        help_text= 'Codigo estado de salida', 
        unique=False,
        null=True
    )
    dx_causa_muerte = models.CharField(
        max_length=20,
        help_text= 'Diagnostico causa muerte', 
        unique=False,
        null=True
    )
    fecha_salida_usuario = models.CharField(
        max_length=22,
        help_text='Fecha salida',
        unique=False,
        null=True,
    )
    hora_salida_usuario = models.CharField(
        max_length=22,
        help_text='Hora salida',
        unique=False,
        null=True,
    )

    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.CharField(
        max_length=30,
        help_text='Fecha creacion',
        unique=False,
        null=True,
    )
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='user_create_ah_int', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.numero_identifacion_usuario)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_fac_ah_int_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_ah_in_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_ah_int_idx'),
            models.Index(fields=['fecha_ingreso_usuario'], name='fecha_ingreso_ah_int_idx'),
        ]
        
        constraints = [
            models.UniqueConstraint(fields=['numero_factura', 'codigo_prestador', 'numero_identifacion_usuario', 'codigo_via_ingreso_institucion', 'fecha_ingreso_usuario', 'hora_ingreso_usuario','codigo_causa_externa','dx_principal_ingreso','dx_principal_egreso','dx_relacionado1_egreso','dx_relacionado2_egreso','dx_relacionado3_egreso','codigo_estado_salida','dx_causa_muerte','fecha_salida_usuario' ], name='registro ah_int unico')
        ] 
        app_label = 'rips'
