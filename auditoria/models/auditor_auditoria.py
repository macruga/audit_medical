# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import noSpacesStartEnd, onlyCharacters, onlyAlphaNumeric, onlyCharactersAndSpaces, onlyCharactersSpacesAndPunctuation, onlyCharactersAndDigits, onlyDigits, onlyDigitsAndPoints, currentDate, rangeDate, facturaType
# importar los elementos de las otras bases de datos


# importar los elementos adicinales del paquete
from auditoria.models.auditor import auditorModel
from auditoria.models.auditoria import auditoriaModel


# modelo de Auditor que realiza una auditoría
class auditorAuditoriaModel (models.Model):
    """
    Modelo de la relación (objeto) AuditorAuditoria, que representa el ejercicio de una auditoría realizada por un auditor

    Attributes
    ----------
    auditor_id: long
        Relación con el modelo de auditor, al auditor que realiza la auditoría
    auditoria_id: long
        Relación con el modelo auditoria, a la auditoría realizada por el auditor
    nota_concurrencia: str
        Texto con la nota de concurrencia hecha por el auditor
    pertinencia_estancia: bool
        Valor para indicar si la estancia es o no pertinente, solo para los roles auditor medico, auditor especialista
    paciente_ventilado: bool
        Valor para indicar si el paciente está ventilado, solo para el rol auditor medico
    hospitalizacion_prevenible: bool
        Valor para indicar si la hospitalización era prevenible, solo para el rol auditor especialista
    """
    auditor_id = models.ForeignKey(
        auditorModel,
        related_name="auditoria_auditor",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column = "auditor_id"
    )
    auditoria_id = models.ForeignKey(
        auditoriaModel,
        related_name = "auditoria_auditoria",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column = "auditoria_id"
    )
    nota_concurrencia = models.TextField(
        max_length=4000,
        help_text="Nota de concurrencia del auditor en al auditoría",
        null=False,
        blank=False,
        validators=[onlyCharactersSpacesAndPunctuation]
    )
    pertinencia_estancia = models.BooleanField(
        help_text="Estancia pertinente",
        blank=True,
        null=True
    )
    paciente_ventilado = models.BooleanField(
        help_text="Paciente ventilado",
        blank=True,
        null=True
    )
    hospitalizacion_prevenible =  models.BooleanField(
        help_text="Indica si la hoispitalización era prevenible",
        blank=True,
        null=True
    )


    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_auditor_auditoria', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.description )
    
    class Meta:
        app_label = 'auditoria'