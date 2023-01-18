# CONSTRUCCIÓN DE MODELOS PENDIENTE
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, onlyCharactersAndDigits, onlyCharacters, onlyDigits, facturaType

# Definicion del modelo para los los rips AP (Procedimientos)
class ApIntermediaModel(models.Model):
    numero_factura = models.CharField(
        max_length=40,
        help_text='Numero de la Factura',
        unique=False,
        null=True
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
    fecha_procedimiento = models.CharField(
        max_length=22,
        help_text='Fecha consulta',
        unique=False,
        null=True,
    )
    numero_autorizacion = models.CharField(
        max_length=30,
        help_text= 'Número de autorización', 
        unique=False,
        null=True
    )    
    codigo_procedimiento = models.CharField(
        max_length=20,
        help_text= 'Codigo procedimiento', 
        unique=False,
        null=True
    )    
    ambito_procedimiento = models.CharField(
        max_length=20,
        help_text= 'Ambito procedimiento', 
        unique=False,
        null=True
    )
    finalidad_procedimiento = models.CharField(
        max_length=20,
        help_text= 'Finalidad procedimiento', 
        unique=False,
        null=True
    )
    codigo_personal_atiende = models.CharField(
        max_length=20,
        help_text= 'Personal que atiende', 
        unique=False,
        null=True
    )
    codigo_diagnostico_principal = models.CharField(
        max_length=20,
        help_text= 'Codigo diagnistico principal', 
        unique=False,
        null=True
    )
    diagnostico_relacionado = models.CharField(
        max_length=20,
        help_text= 'Codigo diagnistico relacionado', 
        unique=False,
        null=True
    )
    complicacion = models.CharField(
        max_length=20,
        help_text= 'Codigo complicacion', 
        unique=False,
        null=True
    )
    forma_realizacion_acto_cx = models.CharField(
        max_length=20,
        help_text= 'Codigo forma realizacion acto cx', 
        unique=False,
        null=True
    )
    
    valor_procedimiento = models.CharField(
        max_length=22,
        help_text= 'Valor del procedimiento', 
        unique=False,
        null=True
    )
    """
    Por cada validacion que el registro pase aumenta el numero de validacion, se debe tomar como
    referencia la linea de validacion de cada archivo, se define esta linea en el modelo de reglas de validacion

    """
    estado_validacion = models.IntegerField(
        help_text='Estado de la validacion del registro',
        default=0,
        null=True,
        validators= [
            MinValueValidator(0),
            MinValueValidator(100),
            ]
    )
    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True, null=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='user_create_af_intermedia', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return '{}'.format( self.numero_factura )

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='num_fac_ap_in_idx'),
            models.Index(fields=['codigo_prestador'], name='cod_prestador_ap_in_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='num_identifacion_ap_in_idx'),
            models.Index(fields=['codigo_procedimiento'], name='cod_procedimiento_ap_in_idx'),
        ]
        # Solo pude existir un numero de factura asociado a un prestador
        constraints = [
            models.UniqueConstraint(fields=['numero_factura', 'codigo_prestador', 'tipo_identificacion_usuario', 'numero_identifacion_usuario', 'codigo_procedimiento', 'ambito_procedimiento', 'finalidad_procedimiento', 'codigo_personal_atiende', 'codigo_diagnostico_principal','diagnostico_relacionado','complicacion','forma_realizacion_acto_cx','valor_procedimiento' ], name='registro ap_int unico')
        ] 
        app_label = 'rips'
