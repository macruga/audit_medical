from django.db import models
from django.conf import settings
# Importaciones propias
# from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersAndSpaces, onlyDigits
from core.models.grupo_perfil import GrupoPerfil 
from core.models.modulos_app import ModuloApp

class PerfilModel(models.Model):
    modulo = models.ForeignKey(ModuloApp, on_delete=models.CASCADE)
    group = models.ForeignKey(GrupoPerfil, on_delete=models.CASCADE)
    read = models.BooleanField(
        help_text='Autorizacion para consultas GET del modelo',
        default=True,
    )
    write = models.BooleanField(
        help_text='Autorizacion GET del modelo',
        default=False,
    )
    update = models.BooleanField(
        help_text='Autorizacion POST del modelo',
        default=False,
    )
    options = models.BooleanField(
        help_text='Autorizacion PUT del modelo',
        default=True,
    )
    delete = models.BooleanField(
        help_text='Autorizacion DELETE del modelo',
        default=False,
    )
    head = models.BooleanField(
        help_text='Autorizacion HEAD del modelo',
        default=True,
    )
    patch = models.BooleanField(
        help_text='Autorizacion PATCH del modelo',
        default=False,
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_prerfil', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )

    class Meta: 
            app_label = 'core'