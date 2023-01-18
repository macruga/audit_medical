from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters
    

# Codigo de clasificación triage Model
class codigoClasificacionTriageModel(models.Model):
    '''
    Modelo de la relación Codigo de clasificación triage
    '''
    codigo = models.CharField(
        max_length=5,
        help_text='Código de la clasificación de triage',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    
    description = models.CharField(
        max_length=200,
        help_text='Descripción del código de la clasificación de triage',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_codigo_clasificacion_triage', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )
    
    class Meta:
        app_label = 'autorizaciones'