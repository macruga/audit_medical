from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters, onlyDigits, onlyCharactersSpacesAndPunctuation,\
                            onlyCharactersAndDigits, facturaType
from core.models.soporte.ips import IpsModel
from core.models.soporte.tipo_documento import TipoDocumentoModel

# Definicion del modelo para los los rips AF (Facturas)
class AfModel(models.Model):       
    codigo_prestador = models.ForeignKey( 
        IpsModel, 
        help_text='Codigo habilitacion del prestador',
        related_name='codigo_prestador_af', 
        on_delete=models.CASCADE 
        )
    prestador = models.CharField(
        max_length=200,
        help_text='Nombre del prestador',
        unique=False,
        null=False,
        validators=[
            onlyCharactersSpacesAndPunctuation
        ]
    )
    # @@ Varchar de dos caracteres
    tipo_documento = models.ForeignKey( 
        TipoDocumentoModel, 
        help_text='Codigo habilitacion del prestador',
        related_name='codigo_prestador_af', 
        on_delete=models.CASCADE 
        )
    # @@ NIT del prestador, maximo 16 caracteres, no debe tener guion
    numero_documento = models.CharField(
        max_length=16,
        help_text='Numero del documento del prestador',
        unique=False,
        null=False,
        validators=[
            onlyCharactersAndDigits
        ]
    )
    numero_factura = models.CharField(
        max_length=30,
        help_text='Numero de la Factura',
        unique=False,
        null=False,
        validators=[
            facturaType
        ]
    )
    # @@ no mayor a la fecha actual
    fecha_expedicion = models.DateField(('Fecha Expedicion'), auto_now=False, auto_now_add=False)
     # @@ no mayor a la fecha actual, no mayor a la fecha final
    fecha_inicio = models.DateField(('Fecha Inicio Facturacion'), auto_now=False, auto_now_add=False)
    # @@ no mayor a la fecha actual, no menor a la fecha de inicio
    fecha_final = models.DateField(('Fecha Finalizacion Facturacion'), auto_now=False, auto_now_add=False)
    # !! Crear Modelo para las eps
    # @@ deebe estar en el listado de las EPB
    codigo_entidad = models.CharField(
        max_length=30,
        help_text='Codigo de la Entidad administradora',
        unique=False,
        null=False,
        validators=[
            facturaType
        ]
    )
    nombre_entidad = models.CharField(
        max_length=200,
        help_text='Nombre de la Entidad administradora',
        unique=False,
        null=False,
        validators=[
            onlyCharactersSpacesAndPunctuation
        ]
    )
    numero_contrato = models.CharField(
        max_length=40,
        help_text='Numero contrato',
        unique=False,
        null=True,
        validators=[
            onlyCharactersAndDigits
        ]
    )
    plan_beneficios = models.CharField(
        max_length=40,
        help_text='Plan Beneficios',
        unique=False,
        null=True,
    )
    numero_poliza = models.CharField(
        max_length=40,
        help_text='Numero Poliza',
        unique=False,
        null=True,
    )
    # @@ Campo de tipo doble, que no tenga valores negativos
    valor_pago_compartido = models.DecimalField(
        help_text='Valor pago compartido',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    # @@ Campo de tipo doble
    valor_comision = models.DecimalField(
        help_text='Valor comision',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    # @@ Campo de tipo doble
    valor_descuentos= models.DecimalField(
        help_text='Valor descuentos',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    # @@ Como validar la contratacion??
    valor_neto_pagar= models.DecimalField(
        help_text='Valor neto a pagar',
        max_digits=20,
        decimal_places=2,
        default=0.00
    )
    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='af_file', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return '{}'.format( self.codigo_prestador )

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_factura_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_idx'),
            models.Index(fields=['numero_documento'], name='numero_documento_idx'),
        ]
        # Solo pude existir un numero de factura asociado a un prestador
        constraints = [
            models.UniqueConstraint(fields=['codigo_prestador', 'numero_factura'], name='factura unica')
        ] 
        app_label = 'rips'
