
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import ContentType, User
from core.models.soporte.ips import IpsModel

# Importaciones propias
from core.validators import noSpacesStartEnd, onlyCharactersAndSpaces, phoneValidator, onlyDigits
"""
En una nueva migracion, deactivar la asociacion con el grupo (import del modelo y campo) 
y realizarla solo despues de crear el modelo del usuario
"""
from core.models.grupo_perfil import GrupoPerfil 

# Extend model for user creating 
class UserModel(AbstractUser):
    # groups = models.ForeignKey(Group, on_delete=models.CASCADE)
    token = models.CharField(max_length=250, blank=True, null=True) 
    empresa = models.CharField(
        max_length=200,
        help_text='Empresa a la que pertenece el usuario',
        unique=False,
        blank=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    cargo = models.CharField(
        max_length=200,
        help_text='Cargo usuario',
        unique=False,
        blank=True,
        null=True,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]

    ) 
    phoneNumberPrefix = models.CharField(
        max_length=3,
        help_text='Prefijo telefono',
        unique=False,
        default='+57',
        validators= [phoneValidator]
    )
    phoneNumber = models.CharField(
        max_length=30,
        help_text='Telefono usuario',
        unique=False,
        blank=False,
        null=False,
        validators= [onlyDigits]
    )
    sesion = models.CharField(
        max_length=200,
        help_text='Sesion activa',
        unique=False,
        null=True,
        blank=True
    )
    group_profile = models.ManyToManyField(
        GrupoPerfil, 
        help_text="Grupo de permisos para el usuario",
        blank=True
        )
    group_ips = models.ManyToManyField(
        IpsModel, 
        help_text="Grupo de IPS asociadas al usuario",
        blank=True
        )
    def __str__(self):
        return '{}'.format( self.username)

    class Meta: 
            app_label = 'core'