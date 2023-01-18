# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits
# importar los elementos de las otras bases de datos
from afiliados.models.afiliacion import AfiliacionModel
from afiliados.models.afiliado import afiliadoModel
from atencion_hc.models.servicio_prestador_asegurador import servicioIPSModel
from core.models.soporte.ips import IpsModel
# from core.models.soporte.cie10 import Cie10Model
from atencion_hc.models.tipo_hospitalizacion import tipoHospitalizacionModel

# Modelo de la Atención
class atencionModel (models.Model):
    '''
    Modelo de la relación (objeto) Atencion
    
    Attributes
    ----------
    id: long
        Identificador de la atención
    afiliado_id: int
        identificador del paciente
    afiliacion_id: int
        identificador de la afiliacion del paciente
    servicio: int
        Identificador del servicio de la atención
    ips_id: int
        identificador de la IPS
    fecha_ingreso: Date
        Fecha de ingreso 
    tipo_ingreso: int
        identificador del tipo de ingreso
    origen_evento: str
        String con la indicación del origen del evento
    fecha_egreso: Date
        Fecha de egreso 
    tipo_egreso: int
        identificador del tipo de egreso
    tipo_hospitalizacion: int
        Identificador del tipo de hospitalización
    dias_atencion: int
        Dias que duro la atención
    numero_medicamentos_total: int
        Número total de medicamentos durante la atención
    numero_insumos_total: int
        Número total de insumos durante la atención
    numero_laboratorios_total: int
        Número total de laboratorios durante la atención
    numero_imagenes_total: int
        Número total de imagenes durante la atención
    numero_procedimientos_total: int
        Número total de procedimientos durante la atención
    numero_interconsultas_total: int
        Número total de interconsultas durante la atención
    '''
    afiliado_id = models.ForeignKey(
        afiliadoModel, 
        related_name='atencion_afiliado', 
        on_delete=models.PROTECT, 
        db_column="afiliado_id"
        )

    afiliacion_id = models.ForeignKey(
        AfiliacionModel, 
        related_name='atencion_afiliacion', 
        on_delete=models.PROTECT, 
        db_column="afiliacion_id",
        blank=True,
        null=True
        )
    
    servicio_ips_id = models.ForeignKey(
        servicioIPSModel, 
        related_name='atencion_servicio_ips', 
        on_delete=models.PROTECT, 
        db_column="servicio_ips_id"
        )

    ips_id = models.ForeignKey(
        IpsModel, 
        related_name='atencion_ips', 
        on_delete=models.PROTECT, 
        db_column="ips_id"
        )

    fecha_ingreso = models.DateField((), auto_now=False, auto_now_add=False, blank=False, null=False, validators=[currentDate])

    tipo_ingreso = models.CharField(
        max_length=120,
        help_text='tipo de ingreso a la atención',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )

    origen_evento = models.CharField(
        max_length=100,
        help_text='origen del evento que causo la atención',
        unique=False,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )

    fecha_egreso = models.DateField((), auto_now=False, auto_now_add=False, blank=True, null=True, validators=[currentDate])

    tipo_egreso = models.CharField(
        max_length=120,
        help_text='tipo de egreso de la atención',
        unique=False,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )

    tipo_hospitalizacion = models.ForeignKey(
        tipoHospitalizacionModel, 
        related_name='atencion_tipo_hospitalizacion', 
        on_delete=models.PROTECT, 
        db_column="tipo_hospitalizacion_id",
        null=True,
        blank=True
        )
    
    dias_atencion = models.PositiveIntegerField(
        help_text='Duración en días de la atención',
        unique=False,
        null=True,
        blank=True,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )

    numero_medicamentos_total = models.PositiveIntegerField(
        help_text='Cantidad de medicamentos durante la atencion',
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )

    numero_insumos_total = models.PositiveIntegerField(
        help_text='Cantidad de insumos durante la atencion',
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )

    numero_laboratorios_total = models.PositiveIntegerField(
        help_text='Cantidad de laboratorios durante la atencion',
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )

    numero_imagenes_total = models.PositiveIntegerField(
        help_text='Cantidad de imagenes diagnósticas durante la atencion',
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )

    numero_interconsultas_total = models.PositiveIntegerField(
        help_text='Cantidad de interconsultas durante la atencion',
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )

    numero_procedimientos_total = models.PositiveIntegerField(
        help_text='Cantidad de procedimientos durante la atencion',
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
        ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'