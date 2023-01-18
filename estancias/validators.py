

'''
Clase de validadores para la creacion, actualizacion y egresos de estancias
Attributes
    ----------
    data_estancia: request
        Request data de la estancia a crear
    
    serializer: serializer
        Serializador de la vista

    update: boolean
        True, para procesar validaciones que aplican solo para actualizar estancias
        False, omite validaciones propias de la actualizacion

    esgreso: boolean
        True, para procesar validaciones que aplican solo para realizar egresos
        False, omite validaciones propias del egreso
'''

from rest_framework.response import Response
from rest_framework import status
from datetime import datetime
from estancias.models.egreso_class import EgresoEstancia
# Import custom models
from estancias.models.estancia import EstanciaModel
from estancias.models.servicios_estancias import ServiciosEstanciaModel
from estancias.serializers.estancia import EgresoSerializer
from censo.models.tipo_habitacion import TipoHabitacionModel
# validators
from estancias.rules import *


class EstanciaValidators:

    def __init__(self, data_estancia: dict, serializer='', ) -> dict:
 
        # Request data
        self.data_estancia = data_estancia
        self.serializer = serializer
        self.estancia_egresada = False


    def validateCreate(self):
        afiliado = self.data_estancia['afiliado_id']  

        _rule1 = EstanciaActivaRule( afiliado ).validate()
        if _rule1[0]:
            return Response(_rule1[1], status=status.HTTP_409_CONFLICT)

        # if (self.data_estancia['fecha_egreso'] not in ['', None]):
        #     self.estancia_egresada = True
        #     _rule2 = EgresoMayorAIngresoRule(
        #          fecha_ingreso=self.data_estancia['fecha_ingreso'], fecha_egreso=self.data_estancia['fecha_egreso'] ).validate()
        #     if _rule2[0]:
        #         return Response(_rule2[1], status=status.HTTP_409_CONFLICT)            
            
        #     _rule3 = CamposEgresoRule( self.data_estancia ).validate()
        #     if _rule3[0]:
        #         return Response(_rule3[1], status=status.HTTP_409_CONFLICT)
        
        _rule4 = RangoEstanciaRule(afiliado,  self.data_estancia['fecha_ingreso'] ).validate()
        if _rule4[0]:
            return Response(_rule4[1], status=status.HTTP_409_CONFLICT)
            

        # TODO libreria para los codigos de error (Crear un JSON con los codigos de error )

        estancia = self.serializer.save()
        servicio = TipoHabitacionModel.objects.get(id=self.data_estancia['tipo_habitacion_id'])
        # Save servicio estancia
        ServiciosEstanciaModel.objects.create(
            estancia_id = estancia,
            tipo_habitacion_id = servicio,
            fecha = self.data_estancia['fecha_ingreso'],
            owner_id = self.data_estancia['owner']
        )
         
        
        if self.estancia_egresada:
            # TODO SI generar error al egresar, realizar accion, si error borrar la estancia y notificar error
            EgresoEstancia( self.serializer.data['id'] ).Egresar()
        
        return Response(self.serializer.data, status=status.HTTP_201_CREATED)


    def validateUpdate(self, pk):
        estancia = EstanciaModel.objects.filter(id = pk).all().values()
        afiliado = estancia[0]['afiliado_id_id']

        _rule1 = EstanciaInactivaRule(pk).validate()
        if _rule1[0]:
            return Response(_rule1[1], status=status.HTTP_409_CONFLICT) 
      
        _rule2 = RangoEstanciaRule(afiliado, self.data_estancia['fecha_ingreso'] ).validate()
        if _rule2[0]:
            return Response(_rule2[1], status=status.HTTP_409_CONFLICT)

        EstanciaModel.objects.filter(id=pk).update(**self.data_estancia)
                
        return Response(self.serializer.data, status=status.HTTP_202_ACCEPTED)

    def anularEgresoValidator(self, pk):
        _rule1 = EstanciaExisteRule(pk).validate()
        if _rule1[0]:
            return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
        _rule2 = EstanciaActivaRule(pk).validate()
        if _rule2[0]:
            return Response(_rule2[1], status=status.HTTP_400_BAD_REQUEST)
        _rule3 = EstanciasActivasRule(pk).validate()
        if _rule3[0]:
            return Response(_rule3[1], status=status.HTTP_400_BAD_REQUEST)
        # TODO esta regla se debe controlar desde la configuracion del modulo, de momento esta siempre activa    
        _rule4 = UltimaEstanciaRule(pk).validate()
        if _rule4[0]:
            return Response(_rule4[1], status=status.HTTP_400_BAD_REQUEST)

        data_update = {
            'fecha_egreso': None,
            'estado': True,
            'dx_egreso': None,
            'condicion_alta_id': None

        }

        serializer = EgresoSerializer(data=data_update)
        if serializer.is_valid():
            EstanciaModel.objects.filter(id=pk).update(**data_update)
            return Response(serializer.data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def egresoValidator(self, pk):
        estancia = EstanciaModel.objects.filter(id = pk).values().last()
        afiliado = estancia['afiliado_id_id']  

        _rule1 = EstanciaInactivaRule( afiliado ).validate()
        if _rule1[0]:
            return Response(_rule1[1], status=status.HTTP_409_CONFLICT)

        
        _rule2 = EgresoMayorAIngresoRule(                
                fecha_ingreso=estancia['fecha_ingreso'], fecha_egreso=self.data_estancia['fecha_egreso'] ).validate()
        if _rule2[0]:
            return Response(_rule2[1], status=status.HTTP_409_CONFLICT)            
        
        _rule3 = CamposEgresoRule( self.data_estancia ).validate()
        if _rule3[0]:
            return Response(_rule3[1], status=status.HTTP_409_CONFLICT)
        data_update = self.data_estancia.dict()
        EstanciaModel.objects.filter(id=pk).update(**data_update)
       
        # TODO SI generar error al egresar, realizar accion, si error borrar la estancia y notificar error
        EgresoEstancia( pk ).Egresar()
        
        return Response(self.serializer.data, status=status.HTTP_201_CREATED)
    
    