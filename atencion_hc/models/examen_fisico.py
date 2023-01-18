# importar las librerias y funciones requeridas
from django.db import models
from django.conf import settings

# importar los elementos del core para validación
from core.validators import onlyDigitsAndPoints
# importar los elementos de las otras bases de datos
from atencion_hc.models.atencion import atencionModel
from atencion_hc.models.sensibilidad_examen_fisico import sensibilidadExamenFisicoModel
from atencion_hc.models.reflejos_examen_fisico import reflejosExamenFisicoModel

# Modelo del examen físico realizado en la atención
class examenFisicoModel(models.Model):
    '''
    Modelo de la relación (objeto) examen físico

    Attributes
    ----------
    id: long
        Identificador del examen físico
    atencion_id: int
        Identificador de la atención a la que se asocia el examen físico
    tension_arterial: double
        valor de la tensión arterial durante el examen
    temperatura: double
        valor de la temperatura
    peso: double
        valor del peso
    talla: double
        valor de la talla
    sensibilidad: int
        Identificador de la escala de sensibilidad
    reflejos: int
        Identificador de la escala de reflejos
    '''
    atencion_id = models.ForeignKey(
        atencionModel, 
        related_name='examen_fisico_atencion', 
        on_delete=models.PROTECT,
        db_column="atencion_id"
        )

    tension_arterial = models.DecimalField(
        help_text='tensión arterial',
        max_digits=4, 
        decimal_places=1, 
        unique=False,
        null=True,
        validators= [
            onlyDigitsAndPoints
        ]
    )

    temperatura = models.DecimalField(
        help_text='temperatura',
        max_digits=3, 
        decimal_places=1, 
        unique=False,
        null=True,
        validators= [
            onlyDigitsAndPoints
        ]
    )

    peso = models.DecimalField(
        help_text='peso',
        max_digits=4, 
        decimal_places=1, 
        unique=False,
        null=True,
        validators= [
            onlyDigitsAndPoints
        ]
    )

    talla = models.DecimalField(
        help_text='Estatura',
        max_digits=4, 
        decimal_places=1, 
        unique=False,
        null=True,
        validators= [
            onlyDigitsAndPoints
        ]
    )

    sensibilidad_id = models.ForeignKey(
        sensibilidadExamenFisicoModel,
        related_name='examen_fisico_sensibilidad', 
        on_delete=models.PROTECT,
        db_column="sensibilidad_id"
        )
        
    reflejos_id = models.ForeignKey(
        reflejosExamenFisicoModel,
        related_name='examen_fisico_reflejos', 
        on_delete=models.PROTECT,
        db_column="reflejos_id"
        )

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_examen_fisico', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )
        # De acuerdo con las instrucciones de Manuel, se debe registrar en el Meta la app a la que pertenece
        class Meta:
            app_label = 'atencion_hc'
