from django.db import models
from django.conf import settings
from core.validators import currentDate, onlyCharactersAndSpaces, noSpacesStartEnd, onlyCharactersAndDigits, onlyCharacters, onlyCharactersSpacesAndPunctuation, onlyDigits, onlyDigitsAndDash, onlyDigitsAndPoints
from django.core.validators import MaxValueValidator, MinValueValidator
from core.models.soporte.atc import AtcModel

# Cums Model 
class CumsModel(models.Model):
    class AntibioticoChoices(models.IntegerChoices):
        NO = 0
        SI = 1

    codigo = models.CharField(
        max_length=200,
        help_text='Codigo cums del medicamento',
        unique=True,
        null=False,
        blank=False,
        validators = [
            noSpacesStartEnd,
            onlyDigitsAndDash
            ]
    )

    expediente_cum = models.CharField( 
        max_length=200,
        help_text='Expediente Cum',
        validators= [
            noSpacesStartEnd,
            onlyDigits
            ] 
    )

    consecutivo_cum = models.IntegerField( 
        help_text='Consecutivo Cum',
        validators= [
            MinValueValidator(0),
            MaxValueValidator(999)
            ] 
    )

    nombre_medicamento = models.CharField(
        max_length = 2000,
        help_text='Nombre del medicamento administrado',
        unique=False,
        null=False,
        blank=False,
        default= 'Sin nombre',
        validators = [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation
            ]
    )   

    descripcion = models.CharField(
        max_length=200,
        help_text='Descripcion comercial del medicamento',
        unique=False,
        null=True,
        blank=False,
        validators = [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation
            ]
    )   

    atc = models.CharField(
         max_length=100,
         help_text='Codigo ATC',
         unique=False,
         blank=False,
         validators= [
             noSpacesStartEnd,
             ]
     )

    descripcion_atc = models.CharField(
        max_length=200,
        help_text='Descripcion Codigo ATC',
        unique=False,
        blank=True,
        null=True,
        validators= [
            noSpacesStartEnd
            ]
    )

    registro_invima = models.CharField(
         max_length=200,
         help_text='Registro Sanitario INVIMA',
         unique=False,
         blank=False,
         null=True,
         #default='Sin registro INVIMA',
         validators= [
             noSpacesStartEnd,
             ]
     )

    principio_activo = models.CharField(
         max_length=200,
         help_text='Principio activo del medicamento',
         unique=False,
         blank=False,
         null=True,
         validators= [
             noSpacesStartEnd,
             onlyCharactersAndDigits
             ]
     )

    via_administracion = models.CharField(
         max_length=100,
         help_text='Via de administracion del medicamento',
         unique=False,
         blank=True,
         null=True,
         validators= [
             noSpacesStartEnd,
             onlyCharactersAndDigits
             ]
     )
    
    antibiotico = models.IntegerField(
      choices=AntibioticoChoices.choices,
      help_text = "1: es antibiotico, 2. no es antibiotico",
      default=0,
      blank = False,
      null=False
  )

    created = models.DateTimeField(
        (), 
        auto_now=False, 
        auto_now_add=True,
        )

    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.descripcion )

    class Meta:
        app_label = 'core'