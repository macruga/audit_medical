# ## ### ##### ####### ########### ############# ################# ################## 
from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters
    

# Plan de servicio de autorización Model
class planServicioModel(models.Model):
    '''
    Modelo de la relación plan de servicio de autorización
    '''
    codigo = models.CharField(
        max_length=2,
        help_text='Código del plan de servicio',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    
    description = models.CharField(
        max_length=200,
        help_text='Descripción del plan de servicio de autorización',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
        
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_plan_servicio_autorizacion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )
    
    class Meta:
        app_label = 'autorizaciones'