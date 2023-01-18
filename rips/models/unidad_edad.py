from django.db import models
from django.conf import settings
from core.validators import onlyCharacters, onlyCharactersAndSpaces, noSpacesStartEnd


# Unidad edad Model 
class UnidadEdadModel(models.Model):
    description = models.CharField(
        max_length=35,
        help_text='Descripcion unidad edad',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
            ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_unidad_edad', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )

    class Meta: 
        app_label = 'rips'