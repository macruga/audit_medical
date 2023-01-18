from django.db import models
from django.conf import settings
from core.models.soporte.cums import CumsModel
from core.validators import noSpacesStartEnd, onlyCharacters, onlyDigits


class EventosModel(models.Model):
    
  '''
    Modelo de la relación (Objeto) Afiliado

    Attributes
    ----------
    categoria: varchar
        Tipo de categoria del evento adverso
    descripcion: varchar
        Descripcion del evento adverso
    create: Date
        Fecha de registro del medicamento
    active: Boolean
        Indica si el medicamento registrado esta activo
    owner: int
        Id del usuario que registro el medicamento
    '''


  categoria = models.CharField(
    null = False,
    blank=False,
    max_length=100,
    help_text="Categoria del evento adverso", 
    db_column = "categoria",
    validators=[noSpacesStartEnd, onlyCharacters],

  )

  descripcion = models.CharField(
      null = False,
      blank=False,
      max_length=500,
      help_text="Descriocion del evento adverso", 
      db_column = "descripcion",
      validators=[noSpacesStartEnd, onlyCharacters],
  )

  created = models.DateTimeField((), auto_now=True)
  active = models.BooleanField(default=True)

  def __str__(self):
        return '{}'.format( self.id )

  class Meta:
    app_label = 'eventos'




