from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters, onlyDigits
from core.models.soporte.tipo_documento import TipoDocumentoModel


# Definicion del modelo para los los rips US (Usuarios)
class UsIntermediaModel(models.Model):    
    # Se verifica que exista
    tipo_identificacion_usuario = models.CharField(
        max_length=2,
        help_text='Tipo de identificacion',
        unique=True,
        null=True,
    )
    numero_identifacion_usuario = models.CharField(
        max_length=16,
        help_text='Numero de identificación del usuario',
        unique=True,
        null=False,
    )
    # Se verifica que exista
    codigo_entidad = models.CharField(
        max_length=30,
        help_text='Codigo de la Entidad administradora',
        unique=False,
        null=True,
    )
    tipo_usuario = models.CharField(
        max_length=2,
        help_text='Tipo de Usuario',
        unique=False,
        null=True,
    )
    # Severifica que exista
    primer_apellido = models.CharField(
        max_length=50,
        help_text='Primer apellido del usuario',
        unique=False,
        null=False,
        validators=[onlyCharactersAndSpaces]
    )
    segundo_apellido = models.CharField(
        max_length=50,
        help_text='Segundo apellido del usuario',
        unique=False,
        null=True,
        validators=[onlyCharactersAndSpaces]
    )
    # Se verifica que exista
    primer_nombre = models.CharField(
        max_length=50,
        help_text='Primer nombre del usuario',
        unique=False,
        null=False,
        validators=[onlyCharactersAndSpaces]
    )
    segundo_nombre = models.CharField(
        max_length=50,
        help_text='Seguno nombre del usuario',
        unique=False,
        null=True,
        validators=[onlyCharactersAndSpaces]
    )

    edad = models.CharField(
        max_length=4,
        help_text='Edad',
        unique=False,
        null=True,
    )
    unidad_edad = models.CharField(
        max_length=2,
        help_text='Unidad edad',
        unique=False,
        null=True,
    )
    sexo = models.CharField(
        max_length=2,
        help_text='Sexo',
        unique=False,
        null=True,
    )
    codigo_departamento_residencia = models.CharField(
        max_length=5,
        help_text='Codigo departamento',
        unique=False,
        null=True,
    )
    codigo_municipio_residencia = models.CharField(
        max_length=5,
        help_text='Codigo municipio',
        unique=False,
        null=True,
    ) 
    zona_residencia = models.CharField(
        max_length=5,
        help_text='Zona residencia',
        unique=False,
        null=True,
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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_us_intermedia', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return '{}'.format(self.numero_identifacion_usuario)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_identifacion_usuario'], name='numero_ident_usuario_int_idx'),
            models.Index(fields=['primer_apellido'], name='primer_apellido_int_idx'),
        ]
        # Solo pude existir un numero de factura asociado a un prestador
        constraints = [
            models.UniqueConstraint(fields=['tipo_identificacion_usuario', 'numero_identifacion_usuario', 'primer_apellido', 'primer_nombre' ], name='registro usuario unico intermedia')
        ] 
        app_label = 'rips'
