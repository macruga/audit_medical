# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from core.validators import currentDate, noSpacesStartEnd, onlyCharactersAndDigits, onlyCharactersSpacesAndPunctuation

# importar los elementos de las otras bases de datos
from auditoria.models.tipo_fallas import tipoFallasAuditoriaModel
from core.models.soporte.cups import CupsModel
from core.models.soporte.cums import CumsModel

# modelo de auditoria concurrente y retrospectiva
class fallasModel (models.Model):
    '''
    Modelo de la relación (objeto) fallas
    
    (agregar descripcion)

    Attributes
    ----------
    tipo_falla
        Número de identificador auto-incremental del tipo de falla
    codigo_cups_falla
        Relacion con la tabla de CUPS 
    codigo_cums_falla
        Relacion con la tabla de CUMS
    observación_falla
        Anotación del "médico" sobre la falla

    '''
    
    tipo_falla_id = models.ForeignKey(
        tipoFallasAuditoriaModel,
        related_name="auditoria_tipo_falla",
        on_delete=models.PROTECT,
        null=False,
        blank=False,
        db_column="tipo_falla_id"
    )
    
    codigo_cups_falla = models.ForeignKey(CupsModel, related_name='codigo_cups_falla', on_delete=models.PROTECT)
    
    codigo_cums_falla = models.ForeignKey(CumsModel, related_name='codigo_cums_falla', on_delete=models.PROTECT)

    observacion_falla = models.TextField(
        help_text="Observacion sobre la falla",
        max_length=300,
        unique=False,
        validators=[
            noSpacesStartEnd, 
        ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_falla', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
    
    class Meta:
        app_label = 'auditoria'

