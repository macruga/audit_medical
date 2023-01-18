
'''
Clase de validadores para la creacion, actualizacion de medicamentos asociados a una estancia
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
# Import custom models
from estancias.models.estancia import EstanciaModel
from medicamentos.models import MedicamentoModel
# validators
from estancias.rules import *
from medicamentos.rules import AsesoriaRule, EstanciaMedicamentoRule, MedicamentoExisteRule, ObjecionRule, PertinenciaRule



class MedicamentoValidator:

    def __init__(self, data: dict, serializer='', ) -> dict: 
        # Request data
        self.data = data
        self.serializer = serializer


    def estanciaMedicamentos(self):
        try:
            _rule1 = EstanciaRule( estancia_id=self.data['estancia_id'] ).validate()
            if _rule1[0]:
                return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
            self.serializer.save()
            return Response(self.serializer.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response( str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def medicamentoUpdateValidator(pk, data: dict):
        try:
            medicamento = MedicamentoModel.objects.get(id=pk)
            if medicamento:
                MedicamentoModel.objects.filter(id = pk).update(**data)
                return Response("Medicamento actualizado.", status=status.HTTP_200_OK) 
        except Exception as e:
            return Response( str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def pertinenciaMedicamentos(self, pk):
        try:
            _rule1 = MedicamentoExisteRule( medicamento_id=pk ).validate()
            if _rule1[0]:
                return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
            _rule2 = EstanciaMedicamentoRule( medicamento_id=pk ).validate()
            if _rule2[0]:
                return Response(_rule2[1], status=status.HTTP_404_NOT_FOUND)
            _rule3 = PertinenciaRule( medicamento_id=pk ).validate()
            if _rule3[0]:
                return Response(_rule3[1], status=status.HTTP_406_NOT_ACCEPTABLE)
            if self.data['pertinencia'] not in [1,2]:
                return Response(
                    "El campo 'pertiencia' solo puede ser 1 (Pertinente) o 2 (No Pertinente).", 
                    status=status.HTTP_406_NOT_ACCEPTABLE)

            data = self.data
            # If pertinencia is 2, then the field objecion is set to 1
            if data['pertinencia'] == 2:
                data['objecion'] = 1            
            data['fecha_pertinencia'] = datetime.now()
            MedicamentoModel.objects.filter(id = pk).update(**data)
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response( str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def asesoriaMedicamentos(self, pk):
        try:
            _rule1 = MedicamentoExisteRule( medicamento_id=pk ).validate()
            if _rule1[0]:
                return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
            _rule2 = EstanciaMedicamentoRule( medicamento_id=pk ).validate()
            if _rule2[0]:
                return Response(_rule2[1], status=status.HTTP_404_NOT_FOUND)
            _rule3 = AsesoriaRule( medicamento_id=pk ).validate()
            if _rule3[0]:
                return Response(_rule3[1], status=status.HTTP_406_NOT_ACCEPTABLE)
            
            data = self.data
            data['solicitud_asesoria'] = 1
            data['fecha_solicitud'] = datetime.now()
            MedicamentoModel.objects.filter(id = pk).update(**data)
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response( str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


    def asesorMedicamentos(self, pk):
        try:
            _rule1 = MedicamentoExisteRule( medicamento_id=pk ).validate()
            if _rule1[0]:
                return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
            _rule2 = EstanciaMedicamentoRule( medicamento_id=pk ).validate()
            if _rule2[0]:
                return Response(_rule2[1], status=status.HTTP_404_NOT_FOUND)
            _rule3 = AsesoriaRule( medicamento_id=pk ).validate()
            if _rule3[0]:
                return Response(_rule3[1], status=status.HTTP_406_NOT_ACCEPTABLE)
            
            data = self.data
            data['solicitud_asesoria'] = 2
            data['fecha_asesoria'] = datetime.now()
            MedicamentoModel.objects.filter(id = pk).update(**data)
            return Response(data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response( str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def objecionMedicamentos(self):
        try:
            _rule1 = MedicamentoExisteRule( medicamento_id=self.data['medicamento_id'] ).validate()
            if _rule1[0]:
                return Response(_rule1[1], status=status.HTTP_404_NOT_FOUND)
            _rule2 = EstanciaMedicamentoRule( medicamento_id=self.data['medicamento_id'] ).validate()
            if _rule2[0]:
                return Response(_rule2[1], status=status.HTTP_404_NOT_FOUND)
            _rule3 = ObjecionRule( medicamento_id=self.data['medicamento_id'] ).validate()
            if _rule3[0]:
                return Response(_rule3[1], status=status.HTTP_406_NOT_ACCEPTABLE)
            
            objecion_id = self.serializer.save()
            print(objecion_id)
            data_update = {}
            data_update['objecion'] = 2
            data_update['objecion_id'] = objecion_id.id
            MedicamentoModel.objects.filter(id = self.data['medicamento_id']).update(**data_update)
            return Response(self.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response( str(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


             