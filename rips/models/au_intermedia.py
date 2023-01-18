# CONSTRUCCIÓN DE MODELOS PENDIENTE
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, onlyCharactersAndDigits, onlyCharacters, onlyDigits, facturaType

# Definicion del modelo para los los rips AU tabla intermedia (Urgencias)
class AuIntermediaModel(models.Model):
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
    codigo_causa_externa = models.CharField(
        max_length=20,
        help_text= 'Codigo caso externa', 
        unique=False,
        null=True
    )
    dx_salida = models.CharField(
        max_length=20,
        help_text= 'Diagnostico de salida', 
        unique=False,
        null=True
    )
    dx_relacionado1_salida = models.CharField(
        max_length=20,
        help_text= 'Diagnostico relacionado 1 de salida', 
        unique=False,
        null=True
    )
    dx_relacionado2_salida = models.CharField(
        max_length=20,
        help_text= 'Diagnostico relacionado 2 de salida', 
        unique=False,
        null=True
    )
    dx_relacionado3_salida = models.CharField(
        max_length=20,
        help_text= 'Diagnostico relacionado 3 de salida', 
        unique=False,
        null=True
    )                                                                            
    codigo_destino_salida_usuario = models.CharField(
        max_length=20,
        help_text= 'Codigo destino a la salida de observacion', 
        unique=False,
        null=True
    )
    codigo_estado_salida = models.CharField(
        max_length=20,
        help_text= 'Codigo estado de salida', 
        unique=False,
        null=True
    )
    causa_basica_muerte = models.CharField(
        max_length=20,
        help_text= 'Causa basica muerte', 
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
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True, null=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='user_create_au_int', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.numero_identifacion_usuario)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_fac_au_in_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_au_in_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_au_in_idx'),
            models.Index(fields=['fecha_ingreso_usuario'], name='fecha_ingreso_au_in_idx'),
        ]
        # Solo pude existir un numero de factura asociado a un prestador
        constraints = [
            models.UniqueConstraint(fields=['numero_factura', 'numero_identifacion_usuario', 'fecha_ingreso_usuario' ], name='registro au_int unico')
        ] 
        app_label = 'rips'
