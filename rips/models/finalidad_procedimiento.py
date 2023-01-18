from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd


# Finalidad procedimiento Model 
class FinalidadProcedimientoModel(models.Model):
    description = models.CharField(
        primary_key=True,
        max_length=20,
        help_text='Descripcion finalidad del procedimiento',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_finalidad_procedimiento', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta: 
        app_label = 'rips'