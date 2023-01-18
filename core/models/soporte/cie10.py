from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharactersAndDigits
from django.core.validators import MaxValueValidator, MinValueValidator


# CIE10 Model 
class Cie10Model(models.Model):
    
    codigo = models.CharField(
        primary_key=True,
        max_length=4,
        help_text='Codigo CIE10',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
            ]
    )

    capitulo = models.IntegerField( 
        help_text='Capitulo CIE10',
        validators= [
            MinValueValidator(0)
            ] 
    )
    
    titulo = models.CharField(
        max_length=250,
        help_text='Descripcion CIE10',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    sindromatico = models.BooleanField(default=False)

    alto_riesgo = models.BooleanField(default=False)

    dias_estancia = models.IntegerField(
        help_text='Dias de estancia',
        validators= [
            MinValueValidator(0),
            MaxValueValidator(999)
            ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_cie10', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )

    class Meta:
        app_label = 'core'
        # Add some validations here