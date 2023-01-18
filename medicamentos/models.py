from django.db import models
from django.conf import settings
from core.models.soporte.cums import CumsModel
from core.models.soporte.tipos_asesores import TiposAsesoresModel
from core.validators import noSpacesStartEnd, onlyDigits
from estancias.models.estancia import EstanciaModel

class MedicamentoModel(models.Model):
  class PertinenciaChoices(models.IntegerChoices):
    PERTINENTE = 1
    NO_PERTIENENTE = 2
    REVISION = 0

  class AsesoriaChoices(models.IntegerChoices):
    NO_REQUERIDO = 0
    REQUERIDO = 1
    REVISADO = 2

  class ObjecionChoices(models.IntegerChoices):
    NO_REQUERIDO = 0
    OBJETAR = 1
    OBJETADO = 2
    
  '''
    Modelo de la relación (Objeto) Afiliado

    Attributes
    ----------
    estancia_id: integer
        Id de la estancia relacionada
    cum: integer
        Id del medicamento relacionado
    Pertinencia: Bool
        Indica la pertinencia del medicamento es 1: pertinente, 2: no pertinente, 0: revision
    fecha_pertinencia: Date
        Fecha de la pertinencia
    observacion_concurrente: text
        Observacion del medico concurrente o auditor
    solicitud_asesoria: Integer
        Indica si se requiere asesoria, 0: no requerido, 2: requerido, 3: revisado
    motivo_revision_asesor = str
        Motivo de la solicitud de asesoria
    fecha_asesoria: Date
        Fecha de la asesoria realizada
    nota_asesor: text
        Nota del asesor
    objetado: int
        Indica si el medicamento esta objetado, 0: revision, 2: objetar, 3: objetado
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
    related_name='estancia_medicamentos',
    help_text="Estancia relacionada", 
    on_delete = models.PROTECT,
    db_column = "estancia_id" 
  )

  cum = models.ForeignKey(
    CumsModel,
    null = False,
    blank=False,
    related_name='cums_medicamentos',
    help_text="Id del registro cums del medicamento relacionada", 
    on_delete = models.PROTECT,
    db_column = "cum" 
  )

  pertinencia = models.IntegerField(
      choices=PertinenciaChoices.choices,
      help_text = "Indica pertinencia. 1: pertiente, 2. no pertinente, 0: revision",
      default=0,
      blank = False,
      null=False
  )

  fecha_pertinencia = models.DateField(
        ("Fecha pertinencia"), 
        auto_now=False, 
        auto_now_add=False,
        blank = True,
        null=True
    )
  
  auditor = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    related_name='auditor_medicamentos',
    blank = True,
    null=True,
    on_delete=models.CASCADE
  )

  observacion_concurrente = models.TextField(
    help_text = "Observaciones concurrentes",
    blank = True,
    null=True
  )

  solicitud_asesoria =  models.IntegerField(
      choices=AsesoriaChoices.choices,
      help_text = "Solicitud asesor. 0: no requerido, 1: requerido, 2: revisado, 3: solicitado",
      default=0,
      blank = False,
      null=False
  )

  especialidad_asesoria = models.ForeignKey(
    TiposAsesoresModel,
    null = True,
    blank=True,
    related_name='tipo_asesoria_medicamentos',
    help_text="Id de la especialidad del asesor relacionada", 
    on_delete = models.PROTECT,
    db_column = "especialidad_asesoria" 
  )

  motivo_revision_asesor = models.TextField(
    help_text="indica porque se necesita revision de un aseror",
    blank = True,
    null=True
  )

  fecha_solicitud = models.DateField(
        ("Fecha solicitud asesoria"), 
        auto_now=False, 
        auto_now_add=False,
        blank = True,
        null=True
    )

  usuario_solicitud = models.ForeignKey(
      settings.AUTH_USER_MODEL, 
      related_name='user_solicitud_asesor_medicamentos',
      blank = True,
      null=True,
      on_delete=models.CASCADE
  )

  nota_asesor = models.TextField(
    help_text = "Nota del asesor",
    blank = True,
    null=True
  )

  fecha_asesoria = models.DateField(
        ("Fecha asesoria"), 
        auto_now=False, 
        auto_now_add=False,
        blank = True,
        null=True
    )

  asesor = models.ForeignKey(
    settings.AUTH_USER_MODEL, 
    related_name='asesor_medicamentos',
    blank = True,
    null=True,
    on_delete=models.CASCADE
  )

  objecion = models.IntegerField(
      choices=ObjecionChoices.choices,
      help_text = "Objecion, 0: en revision, 1: objetar, 2: objetado",
      default=0,
      blank = False,
      null=False
  )

  objecion_id = models.IntegerField(
        help_text='Id objecion',
        unique=False,
        null=True,
        blank=True,
        validators= [
            noSpacesStartEnd,
            onlyDigits,
            ]
    )
  
  created = models.DateTimeField((), auto_now=True)
  active = models.BooleanField(default=True)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_medicamentos', on_delete=models.CASCADE)

  def __str__(self):
        return '{}'.format( self.id )

  class Meta:
    app_label = 'medicamentos'

    constraints = [
      # No se puede reportar un medicamento para una misma estancia el mismo dia
      models.UniqueConstraint(fields=['estancia_id', 'cum','created'], 
      name='No se puede reportar un medicamento para una misma estancia el mismo dia')
    ]


