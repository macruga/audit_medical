# CONSTRUCCIÓN DE MODELOS PENDIENTE

from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters, onlyDigits, facturaType, onlyDigitsAndPoints, \
                            onlyCharactersAndDigits
from core.models.soporte.ips import IpsModel
from core.models.soporte.tipo_documento import TipoDocumentoModel                            
from core.models.soporte.cie10 import Cie10Model
from core.models.soporte.codigos_consulta import CodigosConsultaModel
from rips.models.finalidad_consulta import FinalidadConsultatoModel
from rips.models.causa_externa import CausaExternaModel
from rips.models.tipo_dx_principal import TipoDxPrincipalModel

# Definicion del modelo para los los rips AC (Consultas)
class AcModel(models.Model):   
    numero_factura = models.CharField(
        max_length=30,
        help_text='Numero de la Factura',
        unique=False,
        null=False,
        validators=[
            facturaType
        ]
    )
    codigo_prestador = models.ForeignKey( IpsModel, help_text='Codigo habilitacion del prestador', related_name='codigo_prestador_ac', on_delete=models.CASCADE )
    tipo_identificacion_usuario = models.ForeignKey( TipoDocumentoModel, related_name = "tipo_identificacion_ac", on_delete = models.PROTECT )
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
    
    fecha_consulta = models.DateField(
        ('Fecha Consulta'), 
        auto_now=False, 
        auto_now_add=False
        )

    numero_autorizacion = models.CharField(
        max_length=20,
        help_text= 'Número de autorización',
        validators=[
            facturaType
        ]
        )
    codigo_consulta = models.ForeignKey( CodigosConsultaModel, related_name = "codigo_consulta_ac", on_delete = models.PROTECT )    

    codigo_finalidad_consulta = models.ForeignKey(FinalidadConsultatoModel, related_name='finalidad_consulta_ac', on_delete=models.PROTECT)
    
    codigo_causa_externa = models.ForeignKey(CausaExternaModel, related_name='causa_externa_consulta', on_delete=models.PROTECT)
    
    codigo_diagnostico_principal = models.ForeignKey(Cie10Model, related_name='diagnostico_principal_consulta', on_delete=models.PROTECT)

    codigo_diagnostico_relacionado1 = models.ForeignKey(Cie10Model, related_name='diagnostico_relacionado1_consulta', on_delete=models.PROTECT)

    codigo_diagnostico_relacionado2 = models.ForeignKey(Cie10Model, related_name='diagnostico_relacionado2_consulta', on_delete=models.PROTECT)

    codigo_diagnostico_relacionado3 = models.ForeignKey(Cie10Model, related_name='diagnostico_relacionado3_consulta', on_delete=models.PROTECT)
    
    codigo_tipo_diagnostico_principal = models.ForeignKey(TipoDxPrincipalModel, related_name='tipo_diagnostico_consulta', on_delete=models.PROTECT)
  
    valor_consulta = models.DecimalField(
        help_text='Valor de la consulta',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    valor_cuota_moderadora = models.DecimalField(
        help_text='Valor de la cuota moderadora',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    valor_neto_pagar= models.DecimalField(
        help_text='Valor neto a pagar',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='affiles', on_delete=models.CASCADE )
    
    def __str__(self):
        return '{}'.format(self.numero_factura)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_fac_ac_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_ac_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_ac_idx'),
        ]
        # Solo pude existir un numero de factura asociado a un prestador
        constraints = [
            models.UniqueConstraint(fields=['numero_factura', 'codigo_prestador', 'numero_identifacion_usuario', 'codigo_finalidad_consulta', 'codigo_consulta' ], name='registro consulta unico')
        ] 
        app_label = 'rips'
