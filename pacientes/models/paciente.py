from django.db import models
from django.conf import settings
from core.validators import noSpacesStartEnd


class EstanciaModel(models.Model):
    '''
    TODO se cambia el modelo por estancia
    Modelo para la definicion del objeto paciente

    Attributes
    ----------
    id: int
        Valor numérico auto-incremental identificador unico del paciente en el sistema
    afiliado_id: int
        Identificador del afiliado
    
    '''   

    