# ## ### ##### ####### ########### ############# ################# ################## 
from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters


# Tipo Referencia Model
class tipoReferenciaModel(models.Model):
    '''
    Modelo de la relación tipo de refeerncia, que indica el tipo de referencia o contrareferencia
    '''
    description = models.CharField(
        max_length=17,
        help_text='Descripción del tipo de referencia',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
            ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_tipo_referencia', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'referencia'