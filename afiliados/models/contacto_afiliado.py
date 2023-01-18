from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate, onlyDigits, onlyCharactersAndDigits, onlyCharactersAndSpaces
# importar los elementos de las otras bases de datos
from afiliados.models.afiliado import afiliadoModel

# contacto Model 
class contactoAfiliadoModel(models.Model):
    '''
    Representa la relación contacto de un afiliado

    Attributes
    ----------
    afiliado_id: int
        identificador del afiliado
    telefono1: str
        Número telefónico uno del afiliado
    telefono2: str
        Número telefónico dos del afiliado
    movil1: str
        Número telefónico móvil uno del afiliado
    movil2: str
        Número telefónico móvil dos del afiliado
    email: str
        Correo electrónico del afiliado
    '''
    afiliado_id = models.ForeignKey(
        afiliadoModel, 
        help_text="identificador del afiliado", 
        on_delete=models.PROTECT,
        db_column="afiliado_id"
        )


    telefono1 = models.CharField(
        max_length=50,
        help_text='Telefono 1',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
            ]
    )
    telefono2 = models.CharField(
        max_length=50,
        help_text='Teléfono 2',
        unique=False,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
            ]
    )
    movil1 = models.CharField(
        max_length=50,
        help_text='Teléfono Movil 1',
        unique=False,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
            ]
    )
    movil2 = models.CharField(
        max_length=50,
        help_text='Teléfono Movil 2',
        unique=False,
        null=True,
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

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_contacto_afiliado', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )

    class Meta:
        app_label = 'afiliados'