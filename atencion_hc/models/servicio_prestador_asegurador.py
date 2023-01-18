# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation
# importar los elementos de las otras bases de datos
from core.models.soporte.ips import IpsModel

# Modelo de los servicios de la ips o eps
class servicioIPSModel(models.Model):
    '''
    Modelo de la relación (objeto) Servicio IPS

    Attributes
    ----------
    id: long
        Identificador del servicio de la IPS
    description: str
        Descripcion del servicio de la IPS
    ips_id: int
        Identificador de la IPS que provee el servicio
    '''

    description = models.CharField(
        max_length=120,
        help_text='Descripción servicio IPS',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )
    ips_id = models.ForeignKey(
        IpsModel, 
        related_name='servicio_ips_ips', 
        on_delete=models.PROTECT, 
        db_column="ips_id")

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_servicio_prestador_asegurador', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description  )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'