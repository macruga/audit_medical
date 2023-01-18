from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters, onlyDigits
from core.models.soporte.ips import IpsModel
from core.models.soporte.tipo_documento import TipoDocumentoModel

"""
Este modelo es intermedio a la tabla AF, se encarga de mantener los registros que no
Cumplan con las reglas de validacion, estos registros seran informados a los usuarios para que sean corregidos,
el core validara el ingreso de nuevos registros contra esta tabla intermedia para actalizar aquellos que tuvieran errores
y enviarlos a la tabla principal.

En su mayoria los campos son varchar, y sin relaciones directas a las tablas de soporte

Debe contener minimo el codigo del prestador y el numero de la factura, con estos dos campos se realizara 
el seguimiento para validar la recuperacion o mejora de los datos faltantes


"""

class AfIntermediaModel(models.Model):       
    # Primer parametro unico
    codigo_prestador = models.CharField(
        max_length=15,
        help_text='Codigo del prestador',
        unique=False,
        null=False,
        blank=False,
        validators=[
            onlyDigits
        ]
    )
    prestador = models.CharField(
        max_length=200,
        help_text='Nombre del prestador',
        unique=False,
        null=True,
        blank=True
    )
    tipo_documento = models.CharField(
        max_length=2,
        help_text='Tipo documento prestador',
        unique=False,
        null=True,
        blank=True
    )
    numero_documento = models.CharField(
        max_length=16,
        help_text='Numero del documento del prestador',
        unique=False,
        null=True,
        blank=True
    )
    # Segundo parametro unico
    numero_factura = models.CharField(
        max_length=30,
        help_text='Numero de la Factura',
        unique=False,
        null=False,
        blank=False
    )
    fecha_expedicion = models.CharField(
        max_length=22,
        help_text='Fecha de expedicion de la factura',
        unique=False,
        null=True,
        blank=True
    )
    fecha_inicio = models.CharField(
        max_length=22,
        help_text='Fecha de inicio',
        unique=False,
        null=True,
        blank=True
    )
    fecha_final = models.CharField(
        max_length=22,
        help_text='Fecha final',
        unique=False,
        null=True,
        blank=True
    )
    codigo_entidad = models.CharField(
        max_length=30,
        help_text='Codigo de la Entidad administradora',
        unique=False,
        null=True,
        blank=True
    )
    nombre_entidad = models.CharField(
        max_length=200,
        help_text='Nombre de la Entidad administradora',
        unique=False,
        null=True,
        blank=True
    )
    numero_contrato = models.CharField(
        max_length=40,
        help_text='Numero contrato',
        unique=False,
        null=True,
        blank=True
    )
    plan_beneficios = models.CharField(
        max_length=40,
        help_text='Plan Beneficios',
        unique=False,
        null=True,
        blank=True
    )
    numero_poliza = models.CharField(
        max_length=40,
        help_text='Numero Poliza',
        unique=False,
        default=0,
        null=True,
        blank=True, 
    )
    valor_pago_compartido = models.CharField(
        max_length=15,
        help_text='Valor copago',
        unique=False,
        null=True,
        blank=True, 
    )
    valor_comision = models.CharField(
        max_length=15,
        help_text='Valor comision',
        unique=False,
        null=True,
        blank=True, 
    )
    valor_descuentos= models.CharField(
        max_length=15,
        help_text='Valor descuentos',
        unique=False,
        null=True,
        blank=True, 
    )
    valor_neto_pagar= models.CharField(
        max_length=40,
        help_text='Valor neto a pagar por la entidad contratante',
        unique=False,
        null=True,
        blank=True, 
    )
    valor_neto_pagar = models.CharField(
        max_length=40,
        help_text='Valor neto a pagar por la entidad contratante',
        unique=False,
        null=True,
        blank=True, 
    )

    """
    Por cada validacion que el registro pase aumenta el numero de validacion, se debe tomar como
    referencia la linea de validacion de cada archivo, se define esta linea en el modelo de reglas de validacion

    """
    estado_validacion = models.IntegerField(
        help_text='Estado de la validacion del registro',
        default=0,
        validators= [
            MinValueValidator(0),
            MinValueValidator(100),
            ]
    )
    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='af_file_intermedia', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return '{}'.format( self.codigo_prestador )

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_factura_int_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_int_idx'),
            models.Index(fields=['numero_documento'], name='numero_documento_int_idx'),
        ]
        # Solo pude existir un numero de factura asociado a un prestador
        constraints = [
            models.UniqueConstraint(fields=['codigo_prestador', 'numero_factura'], name='factura unica tabla intermedia')
        ] 
        app_label = 'rips'

