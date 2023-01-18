# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate
# importar los elementos de las otras bases de datos
from atencion_hc.models.atencion import atencionModel
from atencion_hc.models.interconsulta import interconsultaModel

# Modelo de la iterconsulta remitida en la atención
class interconsultaAtencionModel(models.Model):
    '''
    Modelo de la relación (objeto) interconsulta remitida de la atención

    Attributes
    ----------
    id: long
        Identificador de la interconsulta
    atencion_id: int
        Identificador de la atención a la que se asocia la interconsulta
    interconsulta: int
        Identificador de la lista de especialidades de interconsulta
    fecha_orden: date
        fecha en la que fue ordenada la interconsulta
    description: str
        Descripcion de la interconsulta que se ordena
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='interconsulta_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    interconsulta_id = models.ForeignKey(
        interconsultaModel,
        related_name='interconsulta_asociada_atencion', 
        on_delete=models.PROTECT,
        db_column="interconsulta_id"
        )

    fecha_orden = models.DateField(
        ("Fecha remisión interconsulta"), 
        auto_now=False, 
        auto_now_add=False,
        null=False,
        validators = [
            currentDate
        ]
    )

    description = models.CharField(
        max_length=120,
        help_text='Descripción interconsulta remitida',
        unique=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_interconsulta_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
