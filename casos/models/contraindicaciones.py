# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from core.validators import currentDate, noSpacesStartEnd, onlyCharactersAndDigits, onlyCharactersSpacesAndPunctuation



# modelo de auditoria concurrente y retrospectiva
class ContraindicacionModel(models.Model):
    '''
    Modelo de la relación (objeto) Contraindicaciones

    Attributes
    ----------
    id: int
        Número de identificador auto-incremental
    contraindicacion: str
        Contraindicacion sdra
    
    created: Date
        Fecha de carga del registro del censo en el sistema
    owner_id: int 
        Vínculo con la relación de los responsables para la carga del censo
    active: Boolean
        Indica si este registro esta activo o no
    
    '''
   

    contraindicacion = models.CharField(
        max_length=250,
        help_text='Contraindicacion Ecmo',
        null=False,
        validators= [
            noSpacesStartEnd,
            ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_indicacion_sdra', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
    
    class Meta:
        app_label = 'censo'
        # Add some validations here