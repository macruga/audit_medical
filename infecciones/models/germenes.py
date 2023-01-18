
from django.db import models
from django.conf import settings
from core.validators import  noSpacesStartEnd, alphaNumericAndSpaces



# Germenes Model
class GermenModel(models.Model):

    description = models.CharField(
        max_length=200,
        help_text='Nombre del germen',
        unique=True,
        null=False,
        blank=False,
        validators = [
            noSpacesStartEnd,
            alphaNumericAndSpaces
            ]
    )   

    
    created = models.DateTimeField(
        (), 
        auto_now=False, 
        auto_now_add=True
        )

    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )

    class Meta:
        app_label = 'infecciones'