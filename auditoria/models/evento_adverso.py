# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from core.validators import currentDate, noSpacesStartEnd, onlyCharactersAndDigits, onlyCharactersSpacesAndPunctuation

# importar los elementos de las otras bases de datos
from core.models.soporte.tipo_documento import TipoDocumentoModel
from core.models.soporte.cie10 import Cie10Model

from core.models.soporte.ips import IpsModel
from core.models.soporte.cie10 import Cie10Model
from afiliados.models.afiliacion import afiliacionModel
from afiliados.models.afiliado import afiliadoModel

# importar los elementos adicionales del paquete
from auditoria.models.grado_lesion import gradoLesionuditoriaModel
from auditoria.models.tipo_evento_adverso import tipoEventoAdversoAuditoriaModel
from auditoria.models.tipo_requerimiento import tipoRequerimientoAuditoriaModel

# modelo de auditoria concurrente y retrospectiva
class eventoAdversoModel (models.Model):
    '''
    Modelo de la relación (objeto) evento adverso
    
    (agregar descripcion)

    Attributes
    ----------
    tipo_evento_adverso_id: int
        Número de identificador auto-incremental del tipo de evento adverso
    grado_lesion: int
        Relación al grado de lesión [LEVE, MODERADO, GRAVE]
    tipo_de_requerimiento: int
        De acuerdo al tipo de lesion, [Análisis de caso, informe especialista, requerimiento]
    fecha_inicio: Date
        Fecha de inicio de evento adverso
    fecha_fin: Date
        Fecha en que terminó el evento adverso
    observacion_lesion: str
        Anotación del "médico"
    
    '''
    
    tipo_evento_adverso_id = models.ForeignKey(
        tipoEventoAdversoAuditoriaModel,
        related_name="auditoria_tipo_evento_adverso",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="tipo_evento_adverso_id"
    )

    grado_lesion_id = models.ForeignKey(
        gradoLesionuditoriaModel,
        related_name="auditoria_grado_lesion",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="grado_lesion_id"
    )

    tipo_requerimiento = models.ForeignKey(
        tipoRequerimientoAuditoriaModel,
        related_name="auditoria_tipo_requerimiento",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="tipo_requerimiento_id"
    )

    fecha_inicio = models.DateField(
        help_text="Fecha de inicio del evento adeverso",
        auto_now=False,
        auto_now_add=False,
        blank=False,
        null=False,
        validators=[
            currentDate
        ]
    )

    fecha_fin = models.DateField(
        help_text="Fecha en que termino el evento adeverso",
        auto_now=False,
        auto_now_add=False,
        blank=False,
        null=False,
        validators=[
            currentDate
        ]
    )

    observacion_lesion = models.TextField(
        help_text="Anotación del médico",
        max_length=300,
        unique=False,
        validators=[
            noSpacesStartEnd, 
        ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_evento_adverso', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
    
    class Meta:
        app_label = 'auditoria'

