from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces
# importar los elementos de las otras bases de datos
from core.models.soporte.tipo_documento import TipoDocumentoModel
from core.models.soporte.sexo import SexoModel
from core.models.soporte.departamentos import DepartamentoModel
from core.models.soporte.municipios import MunicipioModel
from core.models.soporte.zona_residencia import ZonaResidenciaModel
from core.models.soporte.origen_etnico import OrigenEtnicoModel
from core.models.soporte.paises import PaisModel

# Model para Paciente
class pacienteModel(models.Model):
    '''
    Modelo de la relación (Objeto) Paciente

    Attributes
    ----------
    id_paciente: str
        Identificador unico en el sistema interno
    sexo: str
        Caracter que identifica el sexo del paciente
    fecha_nacimiento: Date
        Fecha de nacimiento del paciente
    fecha_fallecimiento: Date
        Fecha de fallecimiento del paciente
    edad: int
        Edad del paciente
    created: Date
        Fecha de creación del paceinte en el sistema
    cod_pais_residencia: int
        Código del país de residencia
    codigo_departamento: int
        identificador del código de departamento
    codigo_municipio: int
        identificador del código de municipio
    codigo_centro_poblado: int
        identificador del centro poblado
    nombre_pais_residencia: str
        nombre del pais de residencia
    nombre_regional_agrupada_residencia: str
        nombre de la regional
    nombre_division_politica_residencia: str
        nombre del departamento
    nombre_ciudad_residencia: str
        nombre de la ciudad de residencia
    tipo_identificacion: str
        tipo de identificacion del paciente
    identificacion: str
        identificacion del paciente, puede ser de tipo alfanumérico sin espacios
    grupo_etnico: int
        identificador del grupo de pertenecia étnica
    '''
    
    id_paciente = models.CharField(
        max_length=100,
        help_text='identificador del paceinte',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
        ]       
    )
    
    sexo = models.ForeignKey(
        SexoModel, 
        related_name='paciente_sexo', 
        on_delete=models.PROTECT,
        db_column="sexo"
    )

    fecha_nacimiento = models.DateField(
        ("Fecha Nacimiento"), 
        auto_now=False, 
        auto_now_add=False
    )

    fecha_fallecimiento = models.DateField(
        ("Fecha Fallecimiento"), 
        auto_now=False, 
        auto_now_add=False,
        null=True
    )

    edad = models.PositiveIntegerField(
        help_text='Edad del paciente',
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )
    
    fecha_creacion = models.DateTimeField(
        (), 
        auto_now=False, 
        auto_now_add=False
    )
    
    cod_pais_residencia = models.ForeignKey(
        PaisModel,
        related_name="paciente_pais",
        on_delete=models.PROTECT,
        help_text="Código país",
        db_column="cod_pais_residencia"
    )

    cod_division_politica_residencia = models.ForeignKey(
        DepartamentoModel, 
        related_name='paciente_departamento', 
        help_text="Departamento donde reside el paciente", 
        on_delete=models.PROTECT,
        db_column="cod_division_politica_residencia"
    )

    cod_ciudad_residencia = models.ForeignKey(
        MunicipioModel, 
        related_name='paciente_municipio', 
        help_text="Municipio (ciudad) donde reside el paciente",
        on_delete=models.PROTECT,
        db_column="cod_ciudad_residencia"
        )

    nombre_pais_residencia = models.CharField(
        max_length=100,
        help_text='Nombre pais de residencia paciente',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]       
    )

    nombre_regional_agrupada_residencia = models.CharField(
        max_length=100,
        help_text='Nombre regional agrupada paciente',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]       
    )

    nombre_division_politica_residencia = models.CharField(
        max_length=100,
        help_text='Nombre departamento de residencia paciente',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]       
    )

    nombre_ciudad_residencia = models.CharField(
        max_length=100,
        help_text='Nombre ciudad de residencia paciente',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]       
    )
    
    tipo_de_documento = models.ForeignKey(
        TipoDocumentoModel, 
        related_name='paciente_tipo_identificacion',
        on_delete=models.PROTECT,
        unique=False,
        null=False,
        help_text='Tipo de identificación del paciente',
        db_column="tipo_de_documento"
    )
    
    numero_de_documento = models.CharField(
        max_length=100,
        help_text='Identificacion del paciente',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
        ],
        db_column="numero_de_documento"
    )

    grupo_etnico = models.ForeignKey(
        OrigenEtnicoModel, 
        related_name='paciente_pertenencia_etnica', 
        help_text="Pertenencia étnica del paciente", 
        on_delete=models.PROTECT, 
        db_column="grupo_etnico"
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_paciente', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
    
    class Meta:
        app_label = 'medimas'
