"""
Clase para la logica de validaciones del modulo de afiliados


"""

from abc import ABC, abstractmethod
from datetime import datetime
import string
from typing import Dict
from core.validators import rangeDate


class ValidationRule(ABC):
    '''
    Clase Abstracta para definir las diferentes reglas de validación en la creacion de cohortes
    
    Attributes
    ----------
    value: list
        lista de valores que debe ser validados
        
    '''
    def __init__(self):
        ''' Crea un ValidationRule

        Método que instancia un objeto de la clase ValidationRule        
     
        '''
        self.error = False
        self.response_error = {
                    'code': '',
                    'description': '',
                    'data': ''
                }

        
    @abstractmethod
    def validate(self):
        pass

class cohortesRule( ValidationRule ):
    ''' Valida que un id afiliado exista 

        Parameters
        ----------
        data: integer
            Valor que se van a evaluar

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple'''
    
    def __init__(self, data):
        self.data = data # Cohortes data
        print(data)
        ValidationRule.__init__(self)

    def validate(self):
        """
            Validador para la creacion y actualizacion de cohortes
        
        """
        self.response_error['data'] = self.data # Assign data in case of error
        
        try:            
            fecha_ingreso = datetime.strptime(self.data['fecha_ingreso'], "%Y-%m-%d").date()
        except:
            self.response_error = 'La fecha de ingreso no tiene un formato valido'  
            self.error = True          
            return self.error,  self.response_error    
        
        if (self.data['fecha_retiro'] is None) and (self.data['status'] is False):
            self.response_error = 'Si el estado de la cohorte es inactivo, debe indicar una fecha de retiro'
            self.error = True          
            return self.error,  self.response_error 

        if (self.data['fecha_retiro'] is not None):
            try:              
                fecha_retiro = datetime.strptime(self.data['fecha_retiro'], "%Y-%m-%d").date()
            except:
                self.response_error = 'La fecha de retiro no tiene un formato valido'
                self.error = True          
                return self.error,  self.response_error 

            if (self.data['status'] is True):
                self.response_error = 'Se indico una fecha de retiro, por lo tanto el estado de la cohorte debe ser inactivo'
                self.error = True          
                return self.error,  self.response_error 

            try:
                delta_days = rangeDate(date_finish=fecha_retiro, date_start=fecha_ingreso)
            except Exception as err:
                print(err)
                self.response_error = err
                self.error = True          
                return self.error,  self.response_error
        
            if (delta_days < 0):
                self.response_error = 'La fecha de retiro no puede ser menor a la fecha de ingreso a la cohorte'
                self.error = True          
                return self.error,  self.response_error 

        return self.error, self.response_error

