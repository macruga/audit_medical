# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate
# importar los elementos de las otras bases de datos
from atencion_hc.models.atencion import atencionModel


# Modelo de la hoja de anestesia de la atención
class hojaAnestesiaModel(models.Model):
    '''
    Modelo de la relación (objeto) interconsulta remitida de la atención

    Attributes
    ----------
    id: long
        Identificador del examen físico
    atencion_id: int
        Identificador de la atención a la que se asocia el examen físico
    description: str
        Descripcion de la hoja de anestesia
    fecha_hoja: date
        fecha en la que se realiza la hoja de anestesia
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='hoja_anestesia_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    description = models.CharField(
        max_length=120,
        help_text='Descripción hoja de anestesia',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )
    
    fecha_hoja = models.DateField(
        ("Fecha hoja de anestesia"), 
        auto_now=False, 
        auto_now_add=False,
        null=False,
        validators = [
            currentDate
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_hoja_anestesia_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
