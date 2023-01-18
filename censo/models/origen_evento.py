# ## ### ##### ####### ########### ############# ################# ################## 
from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd
    

# Origen del evento censo Model
class OrigenEventoModel(models.Model):
    '''
    Modelo de la relación origen del evento censo

    Attributes
    ----------
    id: int
        Valor numérico auto-incremental para identificar un origen del evento
    description: str
        Texto con la descripción del origen del evento
    '''   
    description = models.CharField(
        max_length=30,
        help_text='Descripción del origen del evento del censo',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_origen_evento_censo', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'censo'
        # Add some validations here