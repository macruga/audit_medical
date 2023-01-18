# CONSTRUCCIÓN DE MODELOS PENDIENTE
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, onlyCharactersAndDigits, onlyCharacters, onlyDigits, facturaType

# Definicion del modelo para los los rips AM (Medicamentos)
class AmIntermediaModel(models.Model):
    numero_factura = models.CharField(
        max_length=200,
        help_text='Numero de la Factura',
        unique=False,
        null=True,
    )
    
    codigo_prestador = models.CharField(
        max_length=200,
        help_text='Codigo del prestador',
        unique=False,
        null=True,
    )
    tipo_identificacion_usuario = models.CharField(
        max_length=200,
        help_text='Tipo de identificacion',
        unique=False,
        null=True,
    )
    numero_identifacion_usuario = models.CharField(
        max_length=200,
        help_text='Numero de identificación del usuario',
        unique=False,
        null=True
    )
    numero_autorizacion = models.CharField(
        max_length=200,
        help_text= 'Número de autorización', 
        unique=False,
        null=True
    )
    codigo_medicamento = models.CharField(
        max_length=200,
        help_text='Codigo Cums',
        unique=False,
        null=True,
    )    
    codigo_tipo_medicamento =  models.CharField(
        max_length=200,
        help_text='Tipo medicamento',
        unique=False,
        null=True,
    )
    nombre_generico_medicamento = models.CharField(
        max_length=300,
        help_text='Nombre genérico del medicamento',
        unique=False,
        null=True,
    )
    forma_farmaceutica = models.CharField(
        max_length=200,
        help_text='Forma farmacéutica',
        unique=False,
        null=True,
    )
    concentracion_medicamento = models.CharField(
        max_length=200,
        help_text='Concentración del medicamento',
        unique=False,
        null=True,
    )
    unidad_medida_medicamento = models.CharField(
        max_length=200,
        help_text='Unidad de medida del medicamento',
        unique=False,
        null=True,
    )
    numero_unidades = models.CharField(
        max_length=100,
        help_text= 'Número de unidades administadas o aplicadas del medicamento', 
        unique=False,
        null=True
    )                                                                         
    valor_unitario_medicamento = models.CharField(
        max_length=100,
        help_text= 'Valor unitario medicamento', 
        unique=False,
        null=True
    )
    valor_total_medicamento = models.CharField(
        max_length=100,
        help_text= 'Valor total medicamento', 
        unique=False,
        null=True
    )

    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True, null=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='user_create_am_int', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return '{}'.format(self.numero_identifacion_usuario)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_fac_am_int_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_am_int_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_am_int_idx'),
            models.Index(fields=['codigo_medicamento'], name='codigo_medicamento_am_int_idx'),
        ]
        
        constraints = [
            models.UniqueConstraint(fields=['numero_factura', 
            'codigo_prestador',
            'numero_identifacion_usuario', 
            'codigo_medicamento', 
            'nombre_generico_medicamento',
            'forma_farmaceutica',
            'unidad_medida_medicamento',
            'concentracion_medicamento',
            'numero_unidades', 
            'valor_total_medicamento' 
            ], name='registro am_int unico')
        ] 
        app_label = 'rips'
