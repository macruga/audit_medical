from django.db import models
from django.conf import settings
# importar los elementos del core para validación
from core.validators import currentDate
# importar los elementos de las otras bases de datos
from afiliados.models.afiliado import afiliadoModel
from core.models.soporte.cohorte import CohorteModel

# cohorte afiliado Model 
class CohorteAfiliadoModel(models.Model):
    '''
    Representa la relación cohorte de un afiliado

    Attributes
    ----------
    afiliado_id: int
        identificador del afiliado
    cohorte_id: int
        identificador de la cohorte
    fecha_ingreso: Date
        fecha en al que el afiliado ingreso a la cohorte
    '''
    afiliado_id = models.ForeignKey(
        afiliadoModel, 
        related_name = "afiliado_cohorte_afiliado",
        help_text="identificador del afiliado", 
        on_delete=models.PROTECT,
        db_column="afiliado_id"
        )

    cohorte_id = models.ForeignKey(
        CohorteModel,
        related_name = "afiliado_cohorte_cohorte",
        help_text = "Cohorte del afiliado",
        on_delete = models.PROTECT,
        db_column = "cohorte_id"
    )

    fecha_ingreso = models.DateField(
        help_text="Fecha de ingreso del afiliado a la cohorte",
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        validators=[
            currentDate
        ]
    )

    fecha_retiro = models.DateField(
        help_text="Fecha de retiro de la cohorte",
        auto_now=False,
        auto_now_add=False,
        blank=True,
        null=True,
        validators=[
            currentDate
        ]
    )

    status = models.BooleanField(default=True)

    created = models.DateTimeField((), auto_now=False, auto_now_add=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_create_cohorte_afiliado', on_delete=models.PROTECT)
    active = models.BooleanField(default=True)

    def __str__(self):
        return '{}'.format( self.id )

    class Meta:
        app_label = 'afiliados'
        constraints = [
            models.UniqueConstraint(fields=['afiliado_id', 'cohorte_id'], name='Las cohortes deben ser unicas para cada afiliado')
        ]
    