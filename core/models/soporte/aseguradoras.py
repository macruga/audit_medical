from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces
from core.models.soporte.regimen import RegimenModel


# Modelo de las aseguradoras o EAPB
class AseguradorasModel(models.Model):
    description = models.CharField(
        max_length=50,
        help_text='Nombre de la Aseguradora',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    nit = models.CharField(
        max_length=50,
        help_text='NIT de la Aseguradora',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
            ]
    )

    habilitado = models.BooleanField(
        help_text='Habilitado',
        default=True
    )

    regimen_id = models.ForeignKey(
        RegimenModel, 
        help_text="regimen de la EAPB",
        related_name="aseguradora_regimen",
        on_delete=models.PROTECT,
        db_column="regimen_id"
    )

    telefono = models.CharField(
        max_length=50,
        help_text='Telefono Movil 1',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
            ]
    )
    email = models.EmailField(
        max_length=100,
        help_text='Correo Electrónico',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            ]
    )
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_aseguradoras_afiliacion', on_delete=models.PROTECT)
    created = models.DateField((), auto_now=False, auto_now_add=True)

    def __str__(self):
        return '{}'.format( self.description )
        
    class Meta:
        app_label = 'afiliados'