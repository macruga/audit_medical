from abc import ABC, abstractmethod
from datetime import datetime
from wsgiref import validate
from core.validators import rangeDate

from eventos.models.eventos_estancias import EventosEstanciaModel


class ValidationRule(ABC):
    '''
    Clase Abstracta para definir las diferentes reglas de validación de las estancias
    
    Attributes
    ----------
    value: list
        lista de valores que debe ser validados
        
    '''
    def __init__(self):
        ''' Crea un ValidationRule

        Método que instancia un objeto de la clase ValidationRule        
     
        '''

        self.validation = False
        self.response_error = {
                    'code': '',
                    'description': '',
                    'data': ''
                }

        
    @abstractmethod
    def validate(self):
        pass

class EventoUnicoRule( ValidationRule ):
    ''' Valida que solo se reporte un mismo evento por estancia el mismo dia 

        Parameters
        ----------
        estancia_id: integer
            Valor que se van a evaluar

        evento_id: integer
            Id del evento reportado

        fecha_evento: Date
            Fecha del evento reportado

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple'''
    
    def __init__(self, estancia_id, evento_id, fecha_evento):
        ValidationRule.__init__(self)
        self.estancia_id = estancia_id
        self.evento_id = evento_id
        self.fecha_evento = fecha_evento

   
    def validate(self):               
        evento = EventosEstanciaModel.objects.filter(
            id = self.estancia_id, evento_id=self.evento_id, fecha_evento=self.fecha_evento).exists()
        if not evento:
            self.response_error.code = '0001'
            self.response_error.description = 'No se puede reportar un mismo evento por estancia el mismo dia '
            return [True, self.response_error]

        return [False, self.response_error]

