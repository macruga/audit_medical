from django.db import models
from django.conf import settings
# from django.contrib.auth.models import User
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits
from core.models.soporte.departamentos import DepartamentoModel


class MunicipioModel(models.Model):
    codigo = models.CharField(
        primary_key=True,
        max_length=5,
        help_text='Codigo Municipio',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
            ]
    )

    description = models.CharField(
        max_length=50,
        help_text='Descripcion municipio',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    departamento_id = models.ForeignKey(
        DepartamentoModel, 
        help_text="Código del departamento", 
        related_name="municipio_departamento", 
        on_delete=models.PROTECT,
        db_column="departamento_id"
        )

    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )

    class Meta:
        app_label = 'core'