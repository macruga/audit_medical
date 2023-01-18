from django.db import models
from django.conf import settings
from core.validators import onlyCharacters, onlyCharactersAndSpaces, noSpacesStartEnd


# Cohorte Model 
class CohorteModel(models.Model):
    '''
    Modelo de la relación cohorte
    '''
    cohorte_id = models.CharField(
        primary_key = True,
        max_length = 3,
        help_text='Codigo cohorte',
        unique = True,
        null = False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
        ]
    )
    

    description = models.CharField(
        max_length=120,
        help_text='Descripcion Cohorte',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_cohorte', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
        
    class Meta:
        app_label = 'core'