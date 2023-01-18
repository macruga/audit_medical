# ## ### ##### ####### ########### ############# ################# ################## 
from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters


# Estado Referencia Model
class estadoReferenciaModel(models.Model):
    '''
    Modelo de la relación estado de referencia o contrareferencia
    '''
    description = models.CharField(
        max_length=50,
        help_text='Estado de la referencia o contrareferencia',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_estado_referencia', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'referencia'    
