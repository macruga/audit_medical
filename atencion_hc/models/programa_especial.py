# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation

# importar los modelos de otras bases 


# Modelo de Programa Especial
class programaEspecialModel(models.Model):
    """
    Modelo de la relación (objeto) programa especial (Cohortes)
    
    Attributes
    ----------
    description: str
        Identificador y descripción del programa especial
    
    """
    description = models.CharField(
        primary_key=True,
        max_length=120,
        help_text='Descripción programa especial',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_programa_especial', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description  )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
