# CONSTRUCCIÓN DE MODELOS PENDIENTE

from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters, onlyDigits, onlyCharactersAndDigits


# Definicion del modelo para los los rips AC (Consultas)
class AcIntermediaModel(models.Model):   
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
    
    fecha_consulta = models.CharField(
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

    codigo_consulta = models.CharField(
        max_length=30,
        help_text= 'Codigo consulta', 
        unique=False,
        null=True
    )
    

    codigo_finalidad_consulta = models.CharField(
        max_length=30,
        help_text= 'Finalidad consulta', 
        unique=False,
        null=True
    )
    
    codigo_causa_externa = models.CharField(
        max_length=30,
        help_text= 'Codigo causa externa', 
        unique=False,
        null=True
    )
    
    codigo_diagnostico_principal = models.CharField(
        max_length=30,
        help_text= 'Codigo dx principal', 
        unique=False,
        null=True
    )

    codigo_diagnostico_relacionado1 = models.CharField(
        max_length=30,
        help_text= 'Codigo dx relacionado 1', 
        unique=False,
        null=True
    )

    codigo_diagnostico_relacionado2 = models.CharField(
        max_length=30,
        help_text= 'Codigo dx relacionado 2', 
        unique=False,
        null=True
    )

    codigo_diagnostico_relacionado3 = models.CharField(
        max_length=30,
        help_text= 'Codigo dx relacionado 3', 
        unique=False,
        null=True
    )

    
    codigo_tipo_diagnostico_principal = models.CharField(
        max_length=30,
        help_text= 'Codigo tipo dx principal', 
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
    valor_consulta = models.CharField(
        max_length=20,
        help_text= 'Valor de la consulta', 
        unique=False,
        null=True
    )
    valor_cuota_moderadora = models.CharField(
        max_length=20,
        help_text= 'Valor cuota moderadora', 
        unique=False,
        null=True
    )
    valor_neto_pagar= models.CharField(
        max_length=20,
        help_text= 'Valor neto a pagar', 
        unique=False,
        null=True
    )
    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True, null=True)
    owner = models.ForeignKey( settings.AUTH_USER_MODEL, related_name='user_create_ac_int', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.numero_factura)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_factura'], name='numero_fac_aci_idx'),
            models.Index(fields=['codigo_prestador'], name='codigo_prestador_aci_idx'),
            models.Index(fields=['numero_identifacion_usuario'], name='numero_identifacion_aci_idx'),
        ]
        # Solo pude existir un numero de factura asociado a un prestador
        constraints = [
            models.UniqueConstraint(fields=['numero_factura', 'fecha_consulta', 'codigo_prestador', 'numero_identifacion_usuario', 'numero_autorizacion', 'codigo_finalidad_consulta', 'codigo_consulta', 'codigo_causa_externa', 'codigo_diagnostico_principal', 'codigo_diagnostico_relacionado1', 'codigo_diagnostico_relacionado2', 'codigo_diagnostico_relacionado3', 'codigo_tipo_diagnostico_principal', 'valor_consulta' ], name='registro consultas_int unico')
        ] 
        app_label = 'rips'
