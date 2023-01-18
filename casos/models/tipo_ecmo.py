# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from core.validators import currentDate, noSpacesStartEnd, onlyCharactersAndDigits, onlyCharactersSpacesAndPunctuation



# modelo de auditoria concurrente y retrospectiva
class TipoEcmoModel (models.Model):
    '''
    Modelo de la relación (objeto) Ecmo, lista de chequeo de los pacientes que están en ECMO

    Attributes
    ----------
    id: int
        Número de identificador auto-incremental
    tipo: str
        Tipo de Ecmo
    
    created: Date
        Fecha de carga del registro del censo en el sistema
    owner_id: int 
        Vínculo con la relación de los responsables para la carga del censo
    active: Boolean
        Indica si este registro esta activo o no
    
    '''
   

    tipo = models.CharField(
        max_length=50,
        help_text='Tipo Ecmo',
        null=False,
        validators= [
            noSpacesStartEnd,
            ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_tipo_ecmo', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
    
    class Meta:
        app_label = 'censo'
        # Add some validations here