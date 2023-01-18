from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces
# importar los elementos de las otras bases de datos
from core.models.soporte.tipo_documento import TipoDocumentoModel
from core.models.soporte.sexo import SexoModel
from core.models.soporte.estado_civil import EstadoCivilModel
from core.models.soporte.departamentos import DepartamentoModel
from core.models.soporte.municipios import MunicipioModel
from core.models.soporte.zona_residencia import ZonaResidenciaModel
from core.models.soporte.ocupacion import OcupacionModel
from core.models.soporte.cif import CifModel
from core.models.soporte.vulnerabilidad import VulnerabilidadModel
from core.models.soporte.origen_etnico import OrigenEtnicoModel
from core.models.soporte.grupo_poblacional import GrupoPoblacionalModel
from core.models.soporte.escolaridad import EscolaridadModel
from core.models.soporte.estados_paciente import EstadosPacienteModel

# Model for Afiliados
class afiliadoModel(models.Model):
    '''
    Modelo de la relación (Objeto) Afiliado

    Attributes
    ----------
    tipo_identificacion: str
        tipo de identificacion del afiliado
    identificacion: str
        identificacion del afiliado, puede ser de tipo alfanumérico sin espacios
    nombres: str
        nombres del afiliado
    primer_apellido: str
        primer apellido del afiliado
    segundo_apellido: str
        segundo apellido del afiliado
    fecha_nacimiento: Date
        Fecha de nacimiento del afiliado
    sexo = str
        Caracter que identifica el sexo del afiliado
    estado_civil: int
        identificador del estado civil
    ocupacion_actual: int
        identificador de la ocupación actual del afiliado según codificación de la OIT
    cohortes: int
        identificador de las cohortes a las que pertenece un afiliado
    discapacidad: int
        identificador de las discapacidades a las que pertenece un afiliado
    codigo_departamento: int
        identificador del código de departamento
    codigo_municipio: int
        identificador del código de municipio
    direccion: str
        dirección de residencia del afiliado
    vulnerabilidad: int
        identificador del nivel de vulnerabilidad
    pertenencia_etnica: int
        identificador del grupo de pertenecia étnica
    grupo_poblacional:int
        identificador del grupo poblacional
    escolaridad: int
        identificador del nivel de escolaridad
    estado_paciente: string[0:1]
        identificador del estado del paciente
    '''
    tipo_identificacion = models.ForeignKey(
        TipoDocumentoModel, 
        related_name='afiliado_tipo_identificacion',
        on_delete=models.CASCADE,
        unique=False,
        null=False,
        help_text='Tipo de identificación del afiliado',
        db_column="tipo_identificacion"
        )

    identificacion = models.CharField(
        max_length=100,
        help_text='Identificacion del afiliado',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]       
    )

    nombres = models.CharField(
        max_length=100,
        help_text='Nombres del afiliado', 
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]       
    )

    primer_apellido = models.CharField(
        max_length=100,
        help_text='Primer apellido', 
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]       
    )

    segundo_apellido = models.CharField(
        max_length=100,
        help_text='Segundo apellido', 
        unique=False,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]       
    )

    fecha_nacimiento = models.DateField(
        ("Fecha Nacimiento"), 
        auto_now=False, 
        auto_now_add=False
    )

    sexo = models.ForeignKey(
        SexoModel, 
        related_name='afiliado_sexo', 
        on_delete=models.PROTECT,
        db_column="sexo"
        )
        
    estado_civil = models.ForeignKey(
        EstadoCivilModel, 
        related_name='afiliado_estado_civil',
        null = True,
        blank = True,
        on_delete=models.PROTECT,
        db_column="estado_civil"
        )

    ocupacion_actual = models.ForeignKey(
        OcupacionModel, 
        related_name='afiliado_ocupacion', 
        null = True,
        blank = True,
        on_delete=models.PROTECT,
        db_column="ocupacion_actual"
        )

    # discapacidad = models.ManyToManyField(CifModel, related_name="discapacidades")
    discapacidad = models.ForeignKey(
        CifModel, 
        related_name="afiliado_discapacidades", 
        null = True,
        blank = True,
        on_delete=models.PROTECT,
        db_column="discapacidad"
        )
    
    codigo_departamento = models.ForeignKey(
        DepartamentoModel, 
        related_name='afiliado_departamento', 
        help_text="Departamento donde reside el afiliado", 
        null = True,
        blank = True,
        on_delete=models.PROTECT,
        db_column="departamento"
        )

    codigo_municipio = models.ForeignKey(
        MunicipioModel, 
        related_name='afiliado_municipio', 
        help_text="Municipio donde reside el afiliado",
        null = True,
        blank = True,
        on_delete=models.PROTECT,
        db_column="municipio"
        )

    codigo_zona_residencial = models.ForeignKey(
        ZonaResidenciaModel, 
        related_name='afiliado_zona_residencial', 
        help_text="Zona donde reside el afiliado",
        null = True,
        blank = True,
        on_delete=models.PROTECT,
        db_column="zona_residencial"
        )

    direccion = models.CharField(
        max_length=220,
        help_text='dirección de residencia del afiliado',
        unique=False,
        null = True,
        blank = True,
        validators= [
            noSpacesStartEnd,
        ]
    )

    vulnerabilidad = models.ForeignKey(
        VulnerabilidadModel, 
        related_name='afiliado_vulnerabilidad',
        help_text='Nivel de vulnerabilidad', 
        null = True,
        blank = True,
        on_delete=models.PROTECT,
        db_column="vulnerabilidad"
        )

    pertenencia_etnica = models.ForeignKey(
        OrigenEtnicoModel, 
        related_name='afiliado_pertenencia_etnica', 
        help_text="Pertenencia étnica", 
        null = True,
        blank = True,
        on_delete=models.PROTECT, 
        db_column="pertenencia_etnica"
    )

    grupo_poblacional = models.ForeignKey(
        GrupoPoblacionalModel, 
        related_name='afiliado_grupo_poblacional', 
        help_text="Grupo poblacional", 
        null = True,
        blank = True,
        on_delete=models.PROTECT,
        db_column="grupo_poblacional"
    )
    
    escolaridad = models.ForeignKey(
        EscolaridadModel, 
        related_name='afiliado_nivel_escolaridad', 
        help_text="Nivel de escolaridad", 
        null = True,
        blank = True,
        on_delete=models.PROTECT,
        db_column="escolaridad"
    )

    estado_paciente = models.ForeignKey(
        EstadosPacienteModel, 
        related_name='estado_paciente_afiliado', 
        help_text="Estado de paciente o vital del afiliado", 
        null = False,
        blank = False,
        default='N',
        on_delete=models.PROTECT,
        db_column="estado_paciente"
    )

#     contacto = models.ForeignKey( contactoModel, on_delete=models.CASCADE)
#     afiliacion = models.ManyToManyField(afiliacionModel, related_name="afiliaciones", blank=True)


    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_afiliado', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    # Solo se permite un numero de identificación asociado a un unico tipo de documento

    
    def __str__(self):
        return '{}'.format( self.id )
    
    class Meta:
        app_label = 'afiliados'
