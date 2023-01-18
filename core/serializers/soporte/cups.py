from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharactersAndDigits, currentDate
from django.core.validators import MaxValueValidator, MinValueValidator


# CUPS Model 
class CupsModel(models.Model):  
    codigo = models.CharField(
        primary_key=True,
        max_length=6,
        help_text='Codigo CUPS',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndDigits,
        ]
    )

    nombre = models.CharField(
        max_length=300,
        help_text='Nombre CUPS',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
        ]
    )

    seccion = models.CharField(
        max_length=120,
        help_text='Sección CUPS',
        unique=False,
        blank=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
        ]
    )
    uso_codigo_rips = models.CharField(
        max_length=5,
        help_text='Uso código CUPS en tablas RIPS',
        unique=False,
        blank=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
        ]
    )
    qx = models.CharField(
        max_length=1,
        help_text='Código CUPS quirúrgico',
        unique=False,
        blank=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
        ]
    )

    numero_minimo = models.IntegerField( 
        help_text='Número Mínimo CUPS',
        blank=True,
        null=True,
        validators= [
            MinValueValidator(0)
            ] 
    )

    numero_maximo = models.IntegerField( 
        help_text='Número Mínimo CUPS',
        blank=True,
        null=True,
        validators= [
            MinValueValidator(0),
            MaxValueValidator(1000)
            ] 
    )
    dx_requerido = models.CharField(
        max_length=1,
        help_text='Diagnóstico requerido CUPS',
        unique=False,
        blank=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
        ]
    )

    capitulo = models.CharField(
        max_length=100,
        help_text='Capítulo CUPS',
        unique=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
        ]
    )
    fecha_actualizacion = models.DateField(
        ("Fecha actualización"), 
        auto_now=False, 
        auto_now_add=False,
        blank=True,
        null=True,
        validators= [
            currentDate
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_cups', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )

    class Meta:
        app_label = 'core'