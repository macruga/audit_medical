# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyCharacters, noSpacesStartEnd, onlyCharactersSpacesAndPunctuation, currentDate
# importar los elementos de las otras bases de datos
from core.models.soporte.cie10 import Cie10Model
from atencion_hc.models.atencion import atencionModel
from atencion_hc.models.tipo_diagnostico import tipoDiagnosticoModel

# Modelo del diagnostico asociado a la atención
class diagnosticoAtencionModel(models.Model):
    '''
    Modelo de la relación (objeto) diagnóstico de la atención

    Attributes
    ----------
    id: long
        Identificador del diagnóstico de la atención
    atencion_id: int
        Identificador de la atención a la que se vincula el diagnóstico
    diagnostico_id: int
        Código CIE 10 del diagnóstico de ingreso
    tipo_diagnostico_id: int
        Descripcion del tipo de ingreso
    fecha: date
        fecha en la que fue realizado el diagnóstico
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='interconsulta_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    diagnostico_id = models.ForeignKey(
        Cie10Model, 
        related_name='diagnostico_cie10_atencion_ingreso', 
        on_delete=models.PROTECT, 
        db_column="diagnostico_id"
        )

    tipo_diagnostico_id = models.ForeignKey(
        tipoDiagnosticoModel,
        related_name='tipo_diagnostico_asociada_atencion', 
        on_delete=models.PROTECT,
        db_column="tipo_diagnostico_id"
        )

    fecha = models.DateField(
        ("Fecha diagnóstico"), 
        auto_now=False, 
        auto_now_add=False,
        null=False,
        validators = [
            currentDate
        ]
    )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_diagnostico_atencion', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'