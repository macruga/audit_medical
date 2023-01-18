from django.db import models
from django.conf import settings
from core.validators import onlyCharacters, noSpacesStartEnd
from rips.models.tipo_archivo import TipoArchivoModel
from rips.models.reglas import reglasModel
from rips.models.tipo_archivo import TipoArchivoModel

# Modelo para la definicion de las reglas de validacion para cada archivo
class reglasValidacionModel(models.Model):
    archivo = models.ForeignKey(TipoArchivoModel, related_name='archivo_validacion', on_delete=models.PROTECT)
    regla = models.ForeignKey(reglasModel, related_name='regla_validacion', on_delete=models.PROTECT)
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_regla_validacion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )

    # Importante agregar esta clase meta en la creacion de cada modelo, para organizacion de la estructura de django
    class Meta: 
        app_label = 'rips'