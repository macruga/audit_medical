from django.db import models
from django.conf import settings
from core.validators import onlyCharactersSpacesAndPunctuation, noSpacesStartEnd, onlyDigits


# Causa externa Model 
class CausaExternaModel(models.Model):
    codigo = models.CharField(
        primary_key=True,
        max_length=2,
        help_text='Codigo causa externa',
        unique=False,
        null=False,
        validators=[
            onlyDigits
        ]
    )
    description = models.CharField(
        max_length=20,
        help_text='Descripcion codigo causa externa',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
            ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_causa_externa', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta: 
        app_label = 'rips'