from django.db import models
from django.conf import settings
from core.validators import onlyCharactersAndSpaces, noSpacesStartEnd


# Personal atencion Model 
class PersonalAtencionModel(models.Model):
    description = models.CharField(
        max_length=20,
        help_text='Descripcion Personal que atiende',
        unique=True,
        null=False,
        validators= [
            noSpacesStartEnd,
            onlyCharactersAndSpaces,
            ]
    )
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_personal_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )

    class Meta: 
        app_label = 'rips'