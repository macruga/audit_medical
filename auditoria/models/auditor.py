# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharacters, onlyAlphaNumeric, onlyCharactersAndSpaces, onlyCharactersSpacesAndPunctuation, onlyCharactersAndDigits, onlyDigits, onlyDigitsAndPoints, currentDate, rangeDate, facturaType
# importar los elementos de las otras bases de datos


# importar los elementos adicinales del paquete
from auditoria.models.rol_auditor import rolAuditorModel


# modelo de Auditor
class auditorModel (models.Model):
    """
    Modelo de la relación (objeto) Auditor

    Attributes
    ----------
    login: str
        Identificador del auditor en la aplicación de auditoria
    nombres: str
        Nombres del auditor
    apellidos: str
        Apellidos del auditor
    rol_auditor_id: long
        Relación con el modelo de roles que indica el rol del auditor 
    """
    login = models.CharField(
        help_text="login del auditor",
        primary_key=True
    )
    
    nombres = models.CharField(
        help_text="Nombre(s) del auditor",
        validators=[
            onlyCharacters,
            noSpacesStartEnd
        ]
    )
    
    apellidos = models.CharField(
        help_text="Apellido(s) del auditor",
        validators=[
            onlyCharacters,
            noSpacesStartEnd
        ]
    )

    rol_auditor_id = models.ForeignKey(
        rolAuditorModel,
        related_name="auditor_rol_auditor",
        on_delete=models.PROTECT,
        db_column="rol_auditor_id"
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_auditor', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'auditoria'