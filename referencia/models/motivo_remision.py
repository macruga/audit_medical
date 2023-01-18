# ## ### ##### ####### ########### ############# ################# ################## 
from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters


# Motivo Remision Model
class motivoRemisionModel(models.Model):
    '''
    Modelo de la relación motivo de remisión de referencia o contrareferencia
    '''
    description = models.CharField(
        max_length=50,
        help_text='Descripción del motivo de remisión',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_motivo_remision', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'referencia' 