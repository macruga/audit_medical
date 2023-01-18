# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation
# importar los elementos de las otras bases de datos


# Modelo de los tipos de diagnostico
class tipoDiagnosticoModel(models.Model):
    '''
    Modelo de la relación (objeto) tipo de diagnóstico

    Attributes
    ----------
    description: str
        Descripcion del tipo de diagnóstico
    '''

    description = models.CharField(
        max_length=15,
        help_text='Descripción tipo de diagnóstico',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersSpacesAndPunctuation,
        ]
    )
    
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_tipo_diagnostico', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description  )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'