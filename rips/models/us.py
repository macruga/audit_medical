from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# importaciones propias
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters, onlyDigits, onlyCharactersAndDigits, facturaType
from core.models.soporte.tipo_documento import TipoDocumentoModel
from rips.models.tipo_usuario import TipoUsuarioModel
from rips.models.unidad_edad import UnidadEdadModel
from core.models.soporte.sexo import SexoModel
from core.models.soporte.departamentos import DepartamentoModel
from core.models.soporte.municipios import MunicipioModel
from core.models.soporte.zona_residencia import ZonaResidenciaModel


# Definicion del modelo para los los rips US (Usuarios)
class UsModel(models.Model):    
    tipo_identificacion_usuario = models.ForeignKey( TipoDocumentoModel, related_name = "tipo_identificacion_usuarios_rips",on_delete = models.PROTECT )
    numero_identifacion_usuario = models.CharField(
        max_length=16,
        help_text='Numero de identificación del usuario',
        unique=True,
        null=False,
        validators=[
            onlyCharactersAndDigits
        ]
    )
    codigo_entidad = models.CharField(
        max_length=30,
        help_text='Codigo de la Entidad administradora',
        unique=False,
        null=False,
        blank=False,
        validators=[
            facturaType
        ]
    )
    tipo_usuario = models.ForeignKey(TipoUsuarioModel, related_name = "tipo_usuario_us", on_delete = models.PROTECT )
    # Se verifica que exista
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
    edad = models.IntegerField(
        help_text='Edad del usuario',
        unique=False,
        null=False,
        validators= [
            MinValueValidator(0),
            MaxValueValidator(120)]
    )
    unidad_edad = models.ForeignKey( UnidadEdadModel, related_name = "unidad_edad_us",on_delete = models.PROTECT )
    sexo = models.ForeignKey( SexoModel, related_name = "sexo_us",on_delete = models.PROTECT )
    codigo_departamento_residencia = models.ForeignKey( DepartamentoModel, related_name = "sexo_us",on_delete = models.PROTECT )
    codigo_municipio_residencia = models.ForeignKey( MunicipioModel, related_name = "sexo_us",on_delete = models.PROTECT ) 
    zona_residencia = models.ForeignKey( ZonaResidenciaModel, related_name = "sexo_us",on_delete = models.PROTECT )

    # radicado = models.ForeignKey( Filing, on_delete=models.CASCADE )
    created = models.DateTimeField(('Fecha de creacion'), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_archivo_us', on_delete=models.CASCADE )
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format(self.numero_identifacion_usuario)

    # Metada dara para definir los indices de la tabla
    class Meta:
        indexes = [
            models.Index(fields=['numero_identifacion_usuario'], name='numero_ident_usuario_idx'),
            models.Index(fields=['primer_apellido'], name='primer_apellido_idx'),
        ]
        # Solo pude existir un numero de factura asociado a un prestador
        constraints = [
            models.UniqueConstraint(fields=['tipo_identificacion_usuario', 'numero_identifacion_usuario', 'primer_apellido', 'primer_nombre'], name='registro usuario unico')
        ] 
        app_label = 'rips'
