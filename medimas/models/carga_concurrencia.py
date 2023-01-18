"""
@Desc: Modelo para realizar la carga de los archivos de concurrencia, usando RESTFUL 

"""

from django.db import models
from django.conf import settings

# Upload File Concurrencia Model 
class uploadFileConcurrenciaModel(models.Model):
    file = models.FileField(max_length=None, upload_to='.')
    procesado = models.BooleanField(default=False)
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_file', on_delete=models.PROTECT)    
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )