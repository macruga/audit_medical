from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharacters


# Regimen Model 
class RegimenModel(models.Model):
    '''
    Modelo de la relación Regimen, que indica el regimen de la afiliación
    '''

    id = models.CharField(
        primary_key = True,
        max_length = 3,
        help_text='Sigla del regimen',
        unique = True,
        null = False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
        ]
    )
    description = models.CharField(
        max_length = 50,
        help_text = 'Descripción del regimen',
        unique = True,
        null = False,
        validators = [
            noSpacesStartEnd,
            onlyCharacters,
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_regimen_afiliacion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'afiliados'