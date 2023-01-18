from django.db import models
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces


# Estados paciente Model 
class TiposAsesoresModel(models.Model):

    description = models.CharField(
        max_length=50,
        help_text='Descripcion del tipo de asesoria',
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
        return '{}'.format( self.id )