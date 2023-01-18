from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd


# Forma de realizacion acto quirurgico Model 
class FormaActoCxModel(models.Model):
    description = models.CharField(
        max_length=40,
        help_text='Descripcion forma realizacion del acto quirurgico',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd
            ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_forma_acto_cx', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )

    class Meta: 
        app_label = 'rips'