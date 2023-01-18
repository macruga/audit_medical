from abc import ABC, abstractmethod
from datetime import datetime
from wsgiref import validate
from core.validators import rangeDate

from estancias.models.estancia import EstanciaModel
from afiliados.models.afiliado import afiliadoModel


class ValidationRule(ABC):
    '''
    Clase Abstracta para definir las diferentes reglas de validación del modulo afiliaciones
    
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

class AfiliadoExisteRule( ValidationRule ):
    ''' Valida que un id afiliado exista 

        Parameters
        ----------
        afiliado_id: integer
            Valor que se van a evaluar

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple'''
    
    def __init__(self, afiliado_id):
        ValidationRule.__init__(self)
        self.afiliado_id = afiliado_id

   
    def validate(self):               
        afiliado = afiliadoModel.objects.filter(id = self.afiliado_id).exists()
        if not afiliado:
            self.response_error.code = '0001'
            self.response_error.description = 'El id de afiliado no existe'
            return [True, self.response_error]

        return [False, self.response_error]
    
    
class AfiliacionMayorVencimientoRule( ValidationRule ):
    ''' Valida los caracteres especiales
        
        Método que valida que la fecha de afiliacion no sea menor a la fecha de vencimiento 

        Parameters
        ----------
        fecha_afiliacion: string
            Fecha de ingreso yyyy-mm-dd

        fecha_vencimiento: string
            Fecha de egreso yyyy-mm-dd

        Returns
        -------
            validation: boolean
            True si existe la regla se cumple

        '''

    def __init__(self, fecha_afiliacion, fecha_vencimiento):
        ValidationRule.__init__(self)
        self.fecha_afiliacion = fecha_afiliacion
        self.fecha_vencimiento = fecha_vencimiento

   
    def validate(self): 
        try:              
            self.fecha_afiliacion = datetime.strptime(self.fecha_afiliacion, "%Y-%m-%d").date()
        except:
            self.fecha_afiliacion = self.fecha_afiliacion
        
        try:              
            self.fecha_vencimiento = datetime.strptime(self.fecha_vencimiento, "%Y-%m-%d").date()
        except:
            self.fecha_vencimiento = self.fecha_vencimiento
        

        # Valida que la fecha de egreso no sea menor a la fecha de ingreso
        if (rangeDate( date_finish=self.fecha_vencimiento, date_start=self.fecha_afiliacion ) < 0):
            self.response_error['code'] = '0002'
            self.response_error['description'] = 'La fecha de vencimiento no puede ser menor a la fecha de afiliacion'
            self.validation = True

        return [self.validation, self.response_error]


