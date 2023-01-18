# ## ### ##### ####### ########### ############# ################# ################## 
from django.db import models
from django.conf import settings
from core.validators import noSpacesStartEnd
    

# Condicion de alta censo Model
class condicionAltaCensoModel(models.Model):
    '''
    Modelo de la relación condición de alta del censo

    Attributes
    ----------
    id: int
        Valor numérico auto-incremental para identificar una condicion de alta
    description: str
        Texto con la descripción de la condición de alta
    '''   
    description = models.CharField(
        max_length=50,
        help_text='Descripción de la condición de alta del censo',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
        ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_condicion_alta_censo', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'censo'