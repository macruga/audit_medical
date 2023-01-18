# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharactersSpacesAndPunctuation

# importar los modelos de otras bases 


# Modelo de sensibilidad examen físico
class sensibilidadExamenFisicoModel(models.Model):
    """
    Modelo de la relación (objeto) sensibilidad para el examen físico
    
    Attributes
    ----------
    description: str
        Identificador y descripción de la sensibilidad 
    
    """
    description = models.CharField(
        primary_key=True,
        max_length=120,
        help_text='Descripción de la sensibilidad',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_sensibilidad_examen_fisico', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description  )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
