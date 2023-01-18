from django.db import models
from django.conf import settings
from django.db.models import Q, F

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, \
     currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces

# from core.models.soporte.departamentos import DepartamentoModel
# from core.models.soporte.municipios import MunicipioModel
# from core.models.soporte.zona_residencia import ZonaResidenciaModel
from core.models.soporte.ips import IpsModel
from core.models.soporte.regimen import RegimenModel
from afiliados.models.afiliado import afiliadoModel
from core.models.soporte.aseguradoras import AseguradorasModel

class AfiliacionModel(models.Model):
    '''
    Modelo que representa la relación (objeto) afiliación

    Attributes
    ----------
    afiliado_id: int
        Identificador del afiliado
    regimen: int
        Regimen de afiliación
    fecha_afiliacion: date
        fecha en que se realizó la afiliación
    fecha vencimiento: date
        fecha en que se da por terminada una afiliación
    status_afiliado: boolean
        indica el estado de la afiliación (True: activa o False: inactiva)
    aseguradora: int
        identificador de la aseguradora a la que se hace la afiliación

    ips_primaria: int
        Identificador de la ips de atencion primaria del paciente

    # codigo_departamento: int
    #     Código del departamento según el DIVIPOLA
    # codigo_municipio: int
    #     Código del municipio según el DIVIPOLA
    # codigo_zona_residencial: int
    #     Código del centro poblado según el DIVIPOLA
    # direccion: str
    #     La dirección del afiliado al momento de realizarse la afiliación
    '''
    afiliado_id = models.ForeignKey(
        afiliadoModel, 
        help_text="identificador del afiliado", 
        on_delete=models.PROTECT,
        db_column="afiliado_id"
        )

    regimen = models.ForeignKey(
        RegimenModel, 
        related_name='regimen_afiliacion', 
        on_delete=models.PROTECT,
        db_column="regimen_id"
        )

    fecha_afiliacion = models.DateField(
        ("Fecha Afiliacion"), 
        auto_now=False, 
        auto_now_add=False,
        blank=False,
        null=False
        )

    fecha_vencimiento = models.DateField(
        ("Fecha vencimiento afiliacion"), 
        auto_now=False, 
        auto_now_add=False,
        blank=False,
        null=False
        )       
    '''
    Los campos en comentarios se retiran el 30/08/2022, se relacionaran los datos demograficos de la afiliacion
    usando los datos de la IPS primaria

    Si el paciente cambia de residencia, se debe actalizar la informacion actual del paciente
    '''    

    # codigo_departamento = models.ForeignKey(
    #     DepartamentoModel, 
    #     related_name='afiliacion_departamento', 
    #     help_text="Departamento donde reside el afilaido", 
    #     on_delete=models.PROTECT,
    #     db_column="departamento_id"
    #     )

    # codigo_municipio = models.ForeignKey(
    #     MunicipioModel, 
    #     related_name='afiliacion_municipio', 
    #     help_text="Municipio donde reside el afiliado",
    #     on_delete=models.PROTECT,
    #     db_column="municipio_id"
    #     )

    # codigo_zona_residencial = models.ForeignKey(
    #     ZonaResidenciaModel, 
    #     related_name='afiliacion_zona_residencial', 
    #     help_text="Zona donde reside el afiliado",
    #     on_delete=models.PROTECT,
    #     db_column="zona_residencial_id"
    #     )

    # direccion = models.CharField(
    #     max_length=220,
    #     help_text='dirección de residencia del afiliado',
    #     unique=False,
    #     null=False,
    #     validators= [
    #         noSpacesStartEnd,
    #     ]
    # )

    # TODO: este campo debe ser manejado dinamicamente, revisar en que momento se debe validar estado de afiliacion
    #       con respecto a la fecha de vencimiento

    status_afiliacion = models.BooleanField( default=True )

    aseguradora_id = models.ForeignKey(
        AseguradorasModel, 
        related_name="aseguradora_afiliacion",
        on_delete=models.PROTECT,
        db_column="aseguradora_id"
        )

    ips_primaria = models.ForeignKey(
        IpsModel, 
        related_name="ips_primaria",
        on_delete=models.PROTECT,
        db_column="ips_primaria"
        )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_afiliacion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        
    class Meta:
        app_label = 'afiliados'
        constraints = [
            # Solo puede existir una afiliacion activa por paciente
            models.UniqueConstraint(fields=['afiliado_id', 'status_afiliacion'], condition=Q(status_afiliacion=True), 
            name='Solo una afiliacion activa por paciente'),
            # Solo puede existir una afiliacion activa por paciente
            models.CheckConstraint(check=Q(fecha_vencimiento__gt=F('fecha_afiliacion')), 
            name='La fecha de vencimiento no puede ser menor o igual a la fecha de afiliacion')
        ]

        # TODO script que automaticamente cambie estatus de afiliacion despues de expirar