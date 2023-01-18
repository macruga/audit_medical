from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd


# Vulnerabilidad Model
# TODO: se debe revisar por completop la forma en que se quiere evaluar la vulnerabilidad, 
#       segun el dane son 5 niveles de vulnerabilidad, que se asocian a diferentes factores (ninguno estrictamente medico)
#       https://visor01.dane.gov.co/visor-vulnerabilidad/
class VulnerabilidadModel(models.Model):
    '''
    Modelo de la relación vulnerabilidad
    '''
    description = models.CharField(
        max_length=30,
        help_text='Descripcion vulnerabilidad',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_vulnerabilidad', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
        
    class Meta:
        app_label = 'core'