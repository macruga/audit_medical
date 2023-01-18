
'''
Clase de validadores para la creacion, actualizacion de eventos adversos asociados a una estancia
Attributes
    ----------
    data: request
        Request data del event a crear o actualizar
    
    serializer: serializer
        Serializador de la vista
'''


from rest_framework.response import Response
from rest_framework import status
# Import custom models
from estancias.models.estancia import EstanciaModel
from medicamentos.models import MedicamentoModel
# validators
from estancias.rules import *
from eventos.rules import *



class EventosValidator:

    def __init__(self, data: dict, serializer='', ) -> dict: 
        # Request data
        self.data = data
        self.serializer = serializer


    def creacionEvento(self):
        '''
        Validador para la creacion de eventos adversos asociados a una estancia
        '''
        try:
            _rule1 = EstanciaRule( estancia_id=self.data['estancia_id'] ).validate()
            if _rule1[0]:
                return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
            _rule2 = FechaMayorAIngresoRule(                
                estancia_id=self.data['estancia_id'], fecha_egreso=self.data['fecha_evento'] ).validate()
            if _rule2[0]:
                return Response(_rule2[1], status=status.HTTP_409_CONFLICT)
            _rule3 = EventoUnicoRule(
                estancia_id=self.data['estancia_id'], evento_id=self.data['evento_id'], fecha_evento=self.data['fecha_evento'] ).validate()
            if _rule3[0]:
                return Response(_rule3[1], status=status.HTTP_409_CONFLICT)
            self.serializer.save()
            return Response(self.serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response( str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    