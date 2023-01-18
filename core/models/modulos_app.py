from django.db import models
from django.conf import settings
# Importaciones propias
from core.validators import noSpacesStartEnd, onlyCharactersAndSpaces, onlyCharacters

class ModuloApp(models.Model):
    modulo = models.CharField(
        max_length=100,
        help_text='Codigo o nombre del modulo',
        unique=True,
        blank=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
            ]
    )
    descripcion = models.CharField(
        max_length=200,
        help_text='Descripcion del modulo',
        unique=True,
        blank=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    ) 
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_modulo_app', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)
    
    def __str__(self):
        return '{}'.format( self.modulo )

    class Meta: 
            app_label = 'core'