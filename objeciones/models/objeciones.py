from django.db import models
from django.conf import settings
from core.models.soporte.cums import CumsModel
from core.models.soporte.cups import CupsModel
from core.models.soporte.tipos_asesores import TiposAsesoresModel
from core.validators import onlyDigitsAndPoints
from estancias.models.estancia import EstanciaModel
from django.core.validators import MaxValueValidator, MinValueValidator
from medicamentos.models import MedicamentoModel
from objeciones.models.tipos_objeciones import TipoObjecionModel

class ObjecionModel(models.Model):
    
    '''
    Modelo de la relación (Objeto) Objeciones

    Attributes
    ----------
    estancia_id: integer
        Id de la estancia relacionada
    cums: integer
        Id del medicamento relacionado
    cups: integer
        Id del procedimiento relacionado
    tipo: integer
        Relacion con tipo de objeciones
    fecha_objecion: Date
        Fecha de la objecion
    nota_objecion: text
        Observacion del medico concurrente o auditor
    valor: Float
        Valor objecion
    cantidad = integer
        Cantidad objetada
    usuario_objecion: integer
        Usuario que realiza la objecion
    create: Date
        Fecha de registro del medicamento
    active: Boolean
        Indica si el medicamento registrado esta activo
    owner: int
        Id del usuario que registro el medicamento
    '''

    estancia_id = models.ForeignKey(
        EstanciaModel,
        null = False,
        blank=False,
        related_name='estancia_objeciones',
        help_text="Estancia relacionada", 
        on_delete = models.PROTECT,
        db_column = "estancia_id" 
    )

    cums = models.ForeignKey(
        CumsModel,
        null = True,
        blank=True,
        related_name='cums_objeciones',
        help_text="Id del registro cums relacionado con la objecion", 
        on_delete = models.PROTECT,
        db_column = "cums" 
    )
    cups = models.ForeignKey(
        CupsModel,
        null = True,
        blank=True,
        related_name='cups_medicamentos',
        help_text="Id del registro cups relacionado con la objecion", 
        on_delete = models.PROTECT,
        db_column = "cups" 
    )

    medicamento_id = models.ForeignKey(
        MedicamentoModel,
        null = True,
        blank=True,
        related_name='medicamento_objeciones',
        help_text="Estancia relacionada", 
        on_delete = models.PROTECT,
        db_column = "medicamento_id" 
    )

    tipo = models.ForeignKey(
        TipoObjecionModel,
        null = False,
        blank=False,
        related_name='objecion_tipo_objecion',
        help_text="Codigo del tipo de objecion", 
        on_delete = models.PROTECT,
        db_column = "tipo" 
    )

    fecha_objecion = models.DateField(
        ("Fecha objecion"), 
        auto_now=False, 
        auto_now_add=False,
        blank = False,
        null=False
    )

    nota_objecion = models.TextField(
    help_text = "Observaciones objecion",
    blank = True,
    null=True
    )

    cantidad =  models.IntegerField(
        help_text = "Solicitud asesor. 0: no requerido, 1: requerido, 2: revisado, 3: solicitado",
        default=1,
        blank = False,
        null=False,
        validators=[
            MaxValueValidator(1000), 
            MinValueValidator(1)
        ]
    )

    valor = models.IntegerField(
        help_text='Valor objecion',
        default=1,
        blank=False,
        null=False,
        validators= [
            MaxValueValidator(100000000), 
            MinValueValidator(1)
        ]
    )

    created = models.DateTimeField((), auto_now=True)
    active = models.BooleanField(default=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_objecion', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format( self.id )

    class Meta:
        app_label = 'objeciones'