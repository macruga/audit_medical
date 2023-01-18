from django.db import models
from django.conf import settings
from core.models.soporte.ips import IpsModel
from django.core.validators import MaxValueValidator, MinValueValidator

# Upload Censo File Model 
class uploadFileCensoModel(models.Model):    

    file = models.FileField(max_length=None, upload_to='.')

    upload_name = models.CharField(
        max_length=100,
        help_text='Nombre del archivo cargado',
        null=False
    )

    ips = models.ForeignKey(
        IpsModel,
        related_name="censo_upload_ips",
        on_delete=models.PROTECT,
        null=False,
        blank=False
    )

    success = models.IntegerField(
        help_text='Registros correctos',
        default=0,
        validators= [
            MinValueValidator(0),
            MaxValueValidator(999)
            ]
    )

    success_file = models.CharField(
        max_length=250,
        help_text='Nombre del archivo con registros correctos',
        null=True,
        blank=True
    )

    success_hash = models.CharField(
        max_length=250,
        help_text='Hash del archivo con registros correctos',
        null=True,
        blank=True
    )

    errors = models.IntegerField(
        help_text='Registros con errores',
        default=0,
        validators= [
            MinValueValidator(0),
            MaxValueValidator(999)
            ]
    )

    errors_file = models.CharField(
        max_length=250,
        help_text='Nombre del archivo de registro con errores',
        null=True,
        blank=True
    )

    errors_hash = models.CharField(
        max_length=250,
        help_text='Hash del archivo de registro con errores',
        null=True,
        blank=True
    )

    errors_json = models.CharField(
        max_length=250,
        help_text='Nombre del archivo de registro con errores en formato JSON',
        null=True,
        blank=True
    )  

    errors_json_hash = models.CharField(
        max_length=250,
        help_text='Hash del archivo de registro con errores en formato json',
        null=True,
        blank=True
    )

    errors_report = models.CharField(
        max_length=250,
        help_text='Reporte de los errores encontrados',
        null=True,
        blank=True
    )

    errors_report_hash = models.CharField(
        max_length=250,
        help_text='Hash del archivo de reporte de los errores encontrados',
        null=True,
        blank=True
    )

    validated = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_file_censo', on_delete=models.PROTECT)    
    # active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )