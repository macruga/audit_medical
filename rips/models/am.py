# CONSTRUCCIÓN DE MODELOS PENDIENTE
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, onlyCharactersAndDigits, onlyCharacters, onlyDigits, facturaType
from core.models.soporte.cums import CumsModel
from rips.models.tipo_medicamento import TipoMedicamentoModel
from core.models.soporte.ips import IpsModel
from core.models.soporte.tipo_documento import TipoDocumentoModel 

# Definicion del modelo para los los rips AM (Medicamentos)
class AmModel(models.Model):
    numero_factura = models.CharField(
        max_length=30,
        help_text='Numero de la Factura',
        unique=False,
        null=False,
        validators=[
            facturaType
        ]
    )
    codigo_prestador = models.ForeignKey( IpsModel, help_text='Codigo habilitacion del prestador', related_name='codigo_prestador_am', on_delete=models.CASCADE )    
    tipo_identificacion_usuario = models.ForeignKey( TipoDocumentoModel, related_name = "tipo_identificacion_am", on_delete = models.PROTECT )
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
    # codigo_medicamento = models.ForeignKey(CumsModel, related_name='cums_medicamentos_am', on_delete=models.PROTECT) 
    codigo_medicamento = models.CharField(
        max_length=100,
        help_text='Codigo medicamento',
        unique=False,
        null=False,
        validators=[
            facturaType
        ]
    )   
    codigo_tipo_medicamento = models.ForeignKey(TipoMedicamentoModel, related_name='cums_am', on_delete=models.PROTECT)
    nombre_generico_medicamento = models.CharField(
        max_length=150,
        help_text='Nombre genérico del medicamento',
        unique=False,
        null=False,
    )
    forma_farmaceutica = models.CharField(
        max_length=100,
        help_text='Forma farmacéutica',
        unique=False,
        null=False,
    )
    concentracion_medicamento = models.CharField(
        max_length=100,
        help_text='Concentración del medicamento',
        unique=False,
        null=False,
    )
    unidad_medida_medicamento = models.CharField(
        max_length=100,
        help_text='Unidad de medida del medicamento',
        unique=False,
        null=False,
    )
    numero_unidades = models.DecimalField(
        help_text='Número de unidades administadas o aplicadas del medicamento',
        max_digits=4,
        decimal_places=1,
        default=0.0
    )                                                                          
    valor_unitario_medicamento = models.DecimalField(
        help_text='Valor unitario de medicamento',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    valor_total_medicamento = models.DecimalField(
        help_text='Valor total de medicamento',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )

    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='user_create_am', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return '{}'.format(self.numero_identifacion_usuario)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_fac_am_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_am_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_am_idx'),
            models.Index(fields=['codigo_medicamento'], name='codigo_medicamento_am_idx'),
        ]
        
        constraints = [
            models.UniqueConstraint(fields=['numero_factura', 'numero_identifacion_usuario', 'codigo_medicamento' ], name='registro medicamento unico')
        ] 
        app_label = 'rips'
