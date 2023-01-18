# CONSTRUCCIÓN DE MODELOS PENDIENTE
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, onlyCharactersAndDigits, onlyCharacters, onlyDigits, facturaType
from core.models.soporte.cups import CupsModel
from rips.models.ambito_procedimiento import AmbitoProcedimientoModel
from rips.models.finalidad_procedimiento import FinalidadProcedimientoModel
from rips.models.personal_atencion import PersonalAtencionModel
from core.models.soporte.cie10 import Cie10Model
from rips.models.forma_realizacion_acto_cx import FormaActoCxModel
from core.models.soporte.ips import IpsModel
from core.models.soporte.tipo_documento import TipoDocumentoModel

# Definicion del modelo para los los rips AP (Procedimientos)
class ApModel(models.Model):
    numero_factura = models.CharField(
        max_length=30,
        help_text='Numero de la Factura',
        unique=False,
        null=False,
        validators=[
            facturaType
        ]
    )
    codigo_prestador = models.ForeignKey( IpsModel, help_text='Codigo habilitacion del prestador', related_name='codigo_prestador_ap', on_delete=models.CASCADE )
    tipo_identificacion_usuario = models.ForeignKey( TipoDocumentoModel, related_name = "tipo_identificacion_ap", on_delete = models.PROTECT )
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
    fecha_procedimiento = models.DateField(('Fecha Procedimiento'), auto_now=False, auto_now_add=False)
    numero_autorizacion = models.CharField(
        max_length=20,
        help_text= 'Número de autorización',
        validators=[
            facturaType
        ]

    )    
    codigo_procedimiento = models.ForeignKey(CupsModel, related_name='cups_ap', on_delete=models.PROTECT)    
    ambito_procedimiento = models.ForeignKey(AmbitoProcedimientoModel, related_name='ambito_procidimiento_ap', on_delete=models.PROTECT)
    finalidad_procedimiento = models.ForeignKey(FinalidadProcedimientoModel, related_name='finalidad_procidimiento_procedimientos', on_delete=models.PROTECT)  
    codigo_personal_atiende = models.ForeignKey(PersonalAtencionModel, related_name='ambito_procidimiento_procedimientos', on_delete=models.PROTECT)
    codigo_diagnostico_principal = models.ForeignKey(Cie10Model, related_name='diagnostico_principal_procedimientos', on_delete=models.PROTECT)
    diagnostico_relacionado = models.ForeignKey(Cie10Model, related_name='diagnostico_relacionado_procedimientos', on_delete=models.PROTECT)
    complicacion = models.ForeignKey(Cie10Model, related_name='complicacion_procedimientos', on_delete=models.PROTECT)
    forma_realizacion_acto_cx = models.ForeignKey(FormaActoCxModel, related_name='forma_realizacion_acto_quirurgico_procedimientos', on_delete=models.PROTECT)
    
    valor_procedimiento = models.DecimalField(
        help_text='Valor del procedimiento',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='user_create_af', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.numero_factura )

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_fac_ap_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_ap_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_ap_idx'),
            models.Index(fields=['codigo_procedimiento'], name='codigo_procedimiento_ap_idx'),
        ]
        # Solo pude existir un numero de factura asociado a un prestador
        constraints = [
            models.UniqueConstraint(fields=['numero_factura', 'codigo_prestador', 'numero_identifacion_usuario', 'codigo_procedimiento' ], name='registro proc unico')
        ] 
        app_label = 'rips'
