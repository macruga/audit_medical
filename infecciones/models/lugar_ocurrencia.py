from django.db import models
from django.conf import settings
from core.validators import  noSpacesStartEnd, alphaNumericAndSpaces
from core.models.soporte.servicios import ServiciosModel


# Lugar ocurrencia Model
class LugarOcurrenciaModel(models.Model):

    description = models.CharField(
        max_length=200,
        help_text='Nombre del lugar de ocurrencia de la infección',
        unique=True,
        null=False,
        blank=False,
        validators = [
            noSpacesStartEnd,
            alphaNumericAndSpaces
            ]
    )   

    servicio = models.ForeignKey(
    ServiciosModel,
    null = False,
    blank=False,
    related_name='tipo_servicio',
    help_text="Id del servicio relacionado", 
    on_delete = models.PROTECT,
    db_column = "id_servicio" 
  )


    created = models.DateTimeField(
        (), 
        auto_now=False, 
        auto_now_add=True,
        )

    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )

    class Meta:
        app_label = 'infecciones'