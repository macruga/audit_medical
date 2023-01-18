from django.db import models
from django.conf import settings
from datetime import date

# Validators
from django.core.validators import MaxValueValidator, MinValueValidator
from core.validators import currentDate

# Custome models
from estancias.models.estancia import EstanciaModel
from censo.models.tipo_habitacion import TipoHabitacionModel


class ServiciosEstanciaModel(models.Model): 
    '''
    Modelo de la relación de los servicios (tipos de habitacion) durante el periodo de estancia

    Attributes
    ----------
    id: int
        Número de identificador auto-incremental
    estancia_id: int
        Vínculo de la relación con la estancia
    fecha: Date
        Fecha donde se registra el paciente en el servicio
    tipo_habitacion_id: int
        Vínculo de la relación con el servicio (tipo de habitacion)
    created: Date
        Fecha de carga del registro del censo en el sistema
    owner_id: int 
        Vínculo con la relación de los responsables para la carga del censo
    active: Boolean
        Indica si este registro esta activo o no
    
    '''

    estancia_id = models.ForeignKey(
        EstanciaModel,
        related_name = "estancia_servicio",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column="estancia_id"
    )

    fecha = models.DateField(
        help_text="Fecha de registro del servicio",
        auto_now=False,
        auto_now_add=False,
        blank=False,
        null=False,
        validators=[
            currentDate
        ]
    )

    tipo_habitacion_id = models.ForeignKey(
        TipoHabitacionModel,
        related_name = "tipo_habitacion_servico_estancia",
        on_delete = models.PROTECT,
        null = False,
        blank = False,
        db_column="tipo_habitacion_id"
    )

   
    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_servicio_estancia', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )

    class Meta:
        app_label = 'estancias'