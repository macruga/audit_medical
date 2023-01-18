from abc import ABC, abstractmethod
from datetime import datetime
from wsgiref import validate
from core.validators import rangeDate
from estancias.models.estancia import EstanciaModel

from medicamentos.models import MedicamentoModel



class ValidationRule(ABC):
    '''
    Clase Abstracta para definir las diferentes reglas de validación de medicamentos
    
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
        self.pertineciasChoices = MedicamentoModel.PertinenciaChoices
        self.asesoriaChoices = MedicamentoModel.AsesoriaChoices
        self.objecionChoices = MedicamentoModel.ObjecionChoices

        
    @abstractmethod
    def validate(self):
        pass

class MedicamentoExisteRule( ValidationRule ):
    ''' Valida que un id de medicamento exista 

        Parameters
        ----------
        medicamento_id: integer
            Valor que se van a evaluar

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple'''
    
    def __init__(self, medicamento_id):
        ValidationRule.__init__(self)
        self.medicamento_id = medicamento_id

   
    def validate(self):               
        medicamento = MedicamentoModel.objects.filter(id = self.medicamento_id).exists()
        if not medicamento:
            self.response_error['code'] = '0001'
            self.response_error['description'] = f'No existe un medicamento registrado con el id: {self.medicamento_id}'
            return [True, self.response_error]

        return [False, self.response_error]

class EstanciaMedicamentoRule( ValidationRule ):
    ''' Valida que un la estancia del medicamento este activa 

        Parameters
        ----------
        medicamento_id: integer
            Valor que se van a evaluar

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple'''
    
    def __init__(self, medicamento_id):
        ValidationRule.__init__(self)
        self.medicamento_id = medicamento_id

   
    def validate(self):
        medicamento = MedicamentoModel.objects.filter(id = self.medicamento_id).values().last()          
        estancia = EstanciaModel.objects.filter(id = medicamento['estancia_id_id'], estado=True).exists()
        if not estancia:
            self.response_error['code'] = '0002'
            self.response_error['description'] = f"La estancia #: {medicamento['estancia_id']} esta inactiva"
            return [True, self.response_error]

        return [False, self.response_error]

class PertinenciaRule( ValidationRule ):
    ''' Valida si se cumple con los requisitos para definir la pertinencia del medicamento 

        Parameters
        ----------
        medicamento_id: integer
            Valor que se van a evaluar

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple'''
    
    def __init__(self, medicamento_id):
        ValidationRule.__init__(self)
        self.medicamento_id = medicamento_id

   
    def validate(self):               
        medicamento = MedicamentoModel.objects.filter(id = self.medicamento_id).values().last()
        if medicamento['solicitud_asesoria'] == 1:
            self.response_error['code'] = '0003'
            self.response_error['description'] = 'No se puede definir pertienencia si existe una solicitud de asesoria pendiente'
            return [True, self.response_error]

        return [False, self.response_error]


class AsesoriaRule( ValidationRule ):
    ''' Valida si se cumple con los requisitos para solicitar asesoria del medicamento 

        Parameters
        ----------
        medicamento_id: integer
            Valor que se van a evaluar

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple'''
    
    def __init__(self, medicamento_id):
        ValidationRule.__init__(self)
        self.medicamento_id = medicamento_id

   
    def validate(self):               
        medicamento = MedicamentoModel.objects.filter(id = self.medicamento_id).values().last()
        if medicamento['pertinencia'] in [1,2]:
            self.response_error['code'] = '0004'
            self.response_error['description'] = 'No se puede solicitar asesoria si el medicamento es pertinente o no pertinente'
            return [True, self.response_error]

        return [False, self.response_error]


class AsesorRule( ValidationRule ):
    ''' Valida si se cumple con los requisitos para realizar la asesoria del medicamento 

        Parameters
        ----------
        medicamento_id: integer
            Valor que se van a evaluar

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple'''
    
    def __init__(self, medicamento_id):
        ValidationRule.__init__(self)
        self.medicamento_id = medicamento_id

   
    def validate(self):               
        medicamento = MedicamentoModel.objects.filter(id = self.medicamento_id).values().last()
        if (medicamento['pertinencia'] in [
                self.pertineciasChoices.PERTINENTE, self.pertineciasChoices.NO_PERTINENTE]):
            self.response_error['code'] = '0004'
            self.response_error['description'] = 'No se puede realizar asesoria si ya se ha definido la pertinencia'
            return [True, self.response_error]
        elif (medicamento['solicitud_asesoria'] == self.asesoriaChoices.NO_SOLICITADO):
            self.response_error['code'] = '0005'
            self.response_error['description'] = 'No se puede realizar la asesoria si no existe una solicitud de asesoria'
            return [True, self.response_error]
        elif (medicamento['solicitud_asesoria'] == self.asesoriaChoices.REVISADO):
            self.response_error['code'] = '0006'
            self.response_error['description'] = 'No se puede realizar la asesoria si ya existe una respuesta de asesoria'
            return [True, self.response_error]

        return [False, self.response_error]


class ObjecionRule( ValidationRule ):
    ''' Valida si se cumple con los requisitos para realizar la objecion del medicamento

        Parameters
        ----------
        medicamento_id: integer
            Valor que se van a evaluar

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple'''
    
    def __init__(self, medicamento_id):
        ValidationRule.__init__(self)
        self.medicamento_id = medicamento_id

   
    def validate(self):               
        medicamento = MedicamentoModel.objects.filter(id = self.medicamento_id).values().last()
        if (medicamento['pertinencia'] in [
                self.pertineciasChoices.PERTINENTE, self.pertineciasChoices.REVISION]):
            self.response_error['code'] = '0007'
            self.response_error['description'] = 'No se puede realizar una objecion si el medicamento es pertinente o en revision'
            return [True, self.response_error]
        elif (medicamento['solicitud_asesoria'] == self.asesoriaChoices.REQUERIDO):
            self.response_error['code'] = '0008'
            self.response_error['description'] = 'No se puede objetar el medicamento si se requiere asesoria'
            return [True, self.response_error]
        elif (medicamento['objecion'] == self.objecionChoices.OBJETADO):
            self.response_error['code'] = '0009'
            self.response_error['description'] = 'No se puede realizar la objecion si ya existe una respuesta de objecion'
            return [True, self.response_error]

        return [False, self.response_error]

