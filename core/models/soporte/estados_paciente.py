from django.db import models
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces


# Estados paciente Model 
class EstadosPacienteModel(models.Model):

    codigo = models.CharField(
        primary_key=True,
        max_length=2,
        help_text='Estado de paciente o vital del afiliado',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharacters,
            ]
    )

    description = models.CharField(
        max_length=50,
        help_text='Descripcion del estado',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.codigo )