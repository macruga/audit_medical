from django.db import models
from core.validators import onlyCharacters, onlyCharactersAndSpaces, noSpacesStartEnd


# Cohorte Model 
class TipoObjecionModel(models.Model):
    '''
    Modelo de la relación cohorte
    '''
    codigo = models.CharField(
        primary_key = True,
        max_length = 4,
        help_text='Codigo objecion',
        unique = True,
        null = False,
        blank = False,
        validators= [
            noSpacesStartEnd
        ]
    )
    
    grupo = models.CharField(
        max_length=100,
        help_text='Grupo objecion',
        unique=False,
        null=False,
        blank=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    description = models.CharField(
        max_length=250,
        help_text='Descripcion objecion',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )
        
    class Meta:
        app_label = 'objeciones'