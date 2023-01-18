from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd


# Destino usuario a la salida de observacion Model 
class EstadoSalidaModel(models.Model):
    description = models.CharField(
        max_length=20,
        help_text='Descripcion estado a la salida',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_estado_salida', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )


    # Importante agregar esta clase meta en la creacion de cada modelo, para organizacion de la estructura de django
    class Meta: 
        app_label = 'rips'