from django.db import models
from django.conf import settings
from core.validators import noSpacesStartEnd, onlyDigits
from estancias.models.estancia import EstanciaModel
from eventos.models.eventos_adversos import EventosModel
from django.db.models import Q, F


class EventosEstanciaModel(models.Model):
    
  '''
    Modelo de la relación (Objeto) Afiliado

    Attributes
    ----------
    estancia_id: integer
        Id de la estancia relacionada
    evento_id: integer
        Id del evento adverso
    fecha_evenot: Date
        Fecha de suceso del evento adverso
    observacion: varchar
        Observaciones del evento adverso 
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
    related_name='estancia_eventos_adversos',
    help_text="Estancia relacionada al evento adverso", 
    on_delete = models.PROTECT,
    db_column = "estancia_id" 
  )

  evento_id = models.ForeignKey(
    EventosModel,
    null = False,
    blank=False,
    related_name='cums_medicamentos',
    help_text="Id del registro cums del medicamento relacionada",
    on_delete = models.PROTECT,
    db_column = "evento_id"
  )

  observacion = models.TextField(
    help_text = "Observaciones del evento",
    blank=False,
    null=False,
    db_column = "observacion" 
  )

  fecha_evento = models.DateField(
    help_text = "Fecha del evento",
    blank=False,
    null=False,
    db_column = "fecha_evento"
  )
  
  created = models.DateTimeField((), auto_now=True)
  active = models.BooleanField(default=True)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_evento_estancia', on_delete=models.CASCADE)

  def __str__(self):
        return '{}'.format( self.id )


  class Meta:
    app_label = 'eventos'

    constraints = [
      # No se puede reportar un mismo evento para una misma estancia el mismo dia
      models.UniqueConstraint(fields=['estancia_id', 'evento_id','fecha_evento'], 
      name='No se puede reportar un mismo evento para una misma estancia el mismo dia')
    ]






# Create your models here.
