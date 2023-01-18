
from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd
    

# Origen del evento censo Model
class TipoHabitacionModel(models.Model):
    '''
    Modelo de la relación tipo de servicio de censo

    Attributes
    ----------
    id: int
        Valor numérico auto-incremental para identificar un tipo de servicio o habitación
    description: str
        Texto con la descripción del servicio o tipo de habitación
    '''   
    description = models.CharField(
        max_length=30,
        help_text='Descripción del tipo de habitación del censo',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_tipo_habitacion_censo', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'censo'