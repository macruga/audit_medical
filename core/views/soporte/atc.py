from django.db import models
from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
# from django.contrib.auth.models import User
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits, onlyCharactersAndDigits


# ATC Model 
class AtcModel(models.Model):
    codigo = models.CharField(
        primary_key=True,
        max_length=10,
        help_text='Código ATC',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )
    nombre = models.CharField(
        max_length=200,
        help_text='Nombre del compuesto del ATC',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    nivel = models.IntegerField(
        help_text='nivel del ATC',
        unique=False,
        null=False,
        validators= [
            MinValueValidator(0)
        ]
    )    
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='usuario_create_atc', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.nombre )

    class Meta:
        app_label = 'core'