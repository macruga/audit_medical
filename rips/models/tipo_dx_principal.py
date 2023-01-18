from django.db import models
from django.conf import settings
from core.validators import onlyCharactersSpacesAndPunctuation, noSpacesStartEnd, onlyDigits


# Tipo diagnostico principal Model 
class TipoDxPrincipalModel(models.Model):
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
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_tipo_dx_ppal', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta: 
        app_label = 'rips'