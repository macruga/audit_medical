from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters
    

# Estado de solicitud de autorización Model
class estadoAutorizacionModel(models.Model):
    '''
    Modelo de la relación estado de la solicitud de autorización
    '''
    description = models.CharField(
        max_length=50,
        help_text='Descripción del estado de la solicitud de autorización',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_estado_solicitud_autorizacion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'autorizaciones'