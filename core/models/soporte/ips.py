from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits
#from core.models.soporte.tipo_documento import TipoDocumentoModel
from core.models.soporte.municipios import MunicipioModel
from core.models.soporte.departamentos import DepartamentoModel


# IPS Model 
class IpsModel(models.Model):
    codigo_habilitacion = models.CharField(
        primary_key=True,
        max_length=50,
        help_text='Codigo Habilitacion',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
            ]
    )
    ips = models.CharField(
        max_length=200,
        help_text='Nombre de la IPS',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    nit = models.CharField(
        max_length=50,
        help_text='Nit de la IPS',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
            ]
    )    
    sucursal = models.CharField(
        max_length=2,
        help_text='Sucursal IPS',
        unique=False,
        null=False,
        default='01',
        validators= [
            noSpacesStartEnd,
            onlyDigits,
            ]
    )
    
    departamento_id = models.ForeignKey(
        DepartamentoModel, 
        related_name="ips_departamento",
        help_text="Codigo del departamento",
        on_delete = models.PROTECT,
        null=True,
        db_column="departamento_id"
    )

    municipio_id = models.ForeignKey(
        MunicipioModel,
        related_name="ips_municipio",
        help_text="Código municipio",
        on_delete = models.PROTECT,
        null=True,
        db_column="municipio_id"
    )

    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='usuario_create_ips', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo_habilitacion )

    class Meta:
        app_label = 'core'