from django.db import models
from django.conf import settings
# Importaciones propias
from core.validators import noSpacesStartEnd, onlyCharactersAndSpaces

class GrupoPerfil(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    descripcion = models.CharField(
        max_length=100,
        help_text='Nombre del grupo de perfil',
        unique=True,
        blank=False,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    ) 
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_grupo_perfil', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.descripcion )

    class Meta: 
            app_label = 'core'