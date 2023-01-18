# ## ### ##### ####### ########### ############# ################# ################## 
from django.db import models
from django.conf import settings
from core.validators import noSpacesStartEnd
    

# Tipo de ingreso al censo Model
class TipoIngresoModel(models.Model):
    '''
    Modelo de la relación tipo de ingreso al censo

    Attributes
    ----------
    id: int
        Valor numérico auto-incremental para identificar un tipo de ingreso al censo
    description: str
        Texto con la descripción del tipo de ingreso al censo
    '''   
    description = models.CharField(
        max_length=40,
        help_text='Descripción del tipo de ingreso del censo',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd
        ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_tipo_ingreso_censo', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'censo'