from abc import ABC, abstractmethod
from datetime import datetime
from wsgiref import validate
from core.validators import rangeDate

from estancias.models.estancia import EstanciaModel
from afiliados.models.afiliado import afiliadoModel


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

class EstanciaRule( ValidationRule ):
    '''         
        Método que valida si existe una estancia y que su estado sea activa

        Parameters
        ----------
        estancia_id: integer
            Id de la estancia a validar

        Returns
        -------
        validation: boolean
            True si existe, la regla se cumple
        '''
    
    def __init__(self, estancia_id):
        ValidationRule.__init__(self)
        self.estancia_id = estancia_id
   
    def validate(self):               
        estancias_activas = EstanciaModel.objects.filter(id=self.estancia_id,estado=True).exists()
        if not estancias_activas:
            self.response_error['code'] = '0011'
            self.response_error['description'] = 'La estancia no existe o no esta activa'
            self.validation = True
        return [self.validation, self.response_error]    
    
class EstanciaActivaRule( ValidationRule ):
    '''         
        Método que valida si existe una estancia activa para el paciente 

        Parameters
        ----------
        afiliado_id: integer
            Valor que se van a evaluar

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple
        '''

    # def __init__(self, fecha_ingreso, fecha_egreso):
    #     self.fecha_ingreso = fecha_ingreso
    #     self.fecha_egreso = fecha_egreso
    
    def __init__(self, afiliado_id):
        ValidationRule.__init__(self)
        self.afiliado_id = afiliado_id

        if AfiliadoExisteRule(afiliado_id).validate()[0]: 
            return [self.validation, self.response_error]

   
    def validate(self):               
        estancias_activas = EstanciaModel.objects.filter(afiliado_id = self.afiliado_id, estado = True).exists()
        if estancias_activas:
            self.response_error['code'] = '0002'
            self.response_error['description'] = 'El paciente ya tiene una estancia activa'
            self.validation = True

        return [self.validation, self.response_error]


class EgresoMayorAIngresoRule( ValidationRule ):
    ''' Valida los caracteres especiales
        
        Método que valida que la fecha de egreso no sea menor a la fecha de ingreso 

        Parameters
        ----------
        fecha_ingreso: string
            Fecha de ingreso yyyy-mm-dd

        fecha_egreso: string
            Fecha de egreso yyyy-mm-dd

        Returns
        -------
            validation: boolean
            True si existe la regla se cumple

        '''

    def __init__(self, fecha_ingreso, fecha_egreso):
        ValidationRule.__init__(self)
        self.fecha_ingreso = fecha_ingreso
        self.fecha_egreso = fecha_egreso

   
    def validate(self): 
        try:              
            self.fecha_egreso = datetime.strptime(self.fecha_egreso, "%Y-%m-%d").date()
        except:
            self.fecha_egreso = self.fecha_egreso
        
        try:              
            self.fecha_ingreso = datetime.strptime(self.fecha_ingreso, "%Y-%m-%d").date()
        except:
            self.fecha_ingreso = self.fecha_ingreso
        

        # Valida que la fecha de egreso no sea menor a la fecha de ingreso
        if (rangeDate( date_finish=self.fecha_egreso, date_start=self.fecha_ingreso ) < 0):
            self.response_error['code'] = '0003'
            self.response_error['description'] = 'La fecha de egreso no puede ser menor a la fecha de ingreso'
            self.validation = True

        return [self.validation, self.response_error]


class FechaMayorAIngresoRule( ValidationRule ):
    ''' Valida los caracteres especiales
        
        Método que valida que la fecha de egreso no sea menor a la fecha de ingreso 

        Parameters
        ----------
        estancia_id: strinintegerg
            Id de la estadía

        fecha: string
            Fecha del evento a reportar yyyy-mm-dd

        Returns
        -------
            validation: boolean
            True si existe la regla se cumple

        '''

    def __init__(self, estancia_id, fecha):
        ValidationRule.__init__(self)
        self.estancia_id = estancia_id
        self.fecha = fecha

   
    def validate(self): 
        try:              
            self.fecha = datetime.strptime(self.fecha, "%Y-%m-%d").date()
        except:
            self.fecha = self.fecha
        

        # Valida que la fecha reportada sea menor a la fecha de ingreso
        estancia = EstanciaModel.objects.filter(id = self.data['estancia_id']).values().last()
        if (rangeDate( date_finish=self.fecha_egreso, date_start=estancia['fecha_ingreso'] ) < 0):
            self.response_error['code'] = '0012'
            self.response_error['description'] = 'La fecha reportada no puede ser menor a la fecha de ingreso'
            self.validation = True

        return [self.validation, self.response_error]


class CamposEgresoRule( ValidationRule ):
    '''         
        Método que valida que la data de la estancia contenga los campos complementarios del egreso:
        condicion_alta, dx_egreso

        Parameters
        ----------
        data: dict
            Datos de la estancia

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple
        '''
    
    def __init__(self, data):
        ValidationRule.__init__(self)
        self.condicion_alta = data['condicion_alta_id']
        self.dx_egreso =  data['dx_egreso']

   
    def validate(self):               
        #  si se marca la fecha de egreso, validar los campos de condicion de alta y dx de egreso como obligatorios
        if (self.condicion_alta  in [None, '']) or (self.dx_egreso in [None, '']):
            self.response_error['code'] = '0004'
            self.response_error['description'] = 'La condición de alta y el dx de egreso son obligatorios'
            self.validation = True

        return [self.validation, self.response_error]


class RangoEstanciaRule( ValidationRule ):
    '''         
        Se valida que las estancias no se traslapen, si el paciente tiene mas de una estancia, la ultima estancia a 
        registrar debe ser mayor a la ultima fecha de egreso

        Parameters
        ----------
        fecha_ingreso: string
            Fecha de egreso yyyy-mm-dd

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple
        '''
    
    def __init__(self, afiliado_id, fecha_ingreso):
        ValidationRule.__init__(self)
        self.fecha_ingreso = fecha_ingreso
        self.afiliado_id = afiliado_id

        if AfiliadoExisteRule(afiliado_id).validate()[0]: 
            return [self.validation, self.response_error]

   
    def validate(self):               
        last_estancia = EstanciaModel.objects.filter(afiliado_id = self.afiliado_id, estado = False).values().last() # Se buscan estancias previas del afiliado
        if ( last_estancia is not None ):
            self.fecha_ingreso = datetime.strptime(self.fecha_ingreso, "%Y-%m-%d")
            if (rangeDate( date_finish=self.fecha_ingreso.date(), date_start=last_estancia['fecha_egreso'] ) <= 0):
                self.response_error['code'] = '0005'
                self.response_error['description'] = 'La fecha de ingreso no puede ser menor o igual a la ultima fecha de egreso del afiliado'
                self.validation = True

        return [self.validation, self.response_error]

class EstanciaInactivaRule( ValidationRule ):
    '''         
        Se valida si la estancia se encuentra inactiva

        Parameters
        ----------
        estancia_id: integer
            Id de la estancia

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple
        '''
    
    def __init__(self, estancia_id):
        ValidationRule.__init__(self)
        self.estancia_id = estancia_id

   
    def validate(self):               
        estancia_inactiva =  EstanciaModel.objects.filter(id = self.estancia_id, estado = False).exists()
        if estancia_inactiva:
            self.response_error['code'] = '0006'
            self.response_error['description'] = 'No puede editar una estancia inactiva, debe anular el egreso para continuar'
            self.validation = True

        return [self.validation, self.response_error]


class EstanciaExisteRule( ValidationRule ):
    ''' Valida si existen el id de estancia

        Parameters
        ----------
        estancia_id: integer
            Valor que se van a evaluar

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple'''
    
    def __init__(self, estancia_id):
        ValidationRule.__init__(self)
        self.estancia_id = estancia_id

   
    def validate(self):               
        estancia = EstanciaModel.objects.filter(id = self.estancia_id).exists()
        if not estancia:
            self.response_error['code'] = '0007'
            self.response_error['description'] = f'No existe una estancia con ID {self.estancia_id}'
            return [True, self.response_error]

        return [False, self.response_error]


class EstanciasActivasRule( ValidationRule ):
    ''' Valida que si existen estancias activas para un afiliado relacionado a un id de estancia

        Parameters
        ----------
        estancia_id: integer
            Valor que se van a evaluar

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple'''
    
    def __init__(self, estancia_id):
        ValidationRule.__init__(self)
        self.estancia_id = estancia_id

   
    def validate(self): 
        # TODO: Validar que el afiliado exista   
        estancia = EstanciaModel.objects.filter(id = self.estancia_id).all().values()
        afiliado = estancia[0]['afiliado_id_id']
        estancias_activas = EstanciaModel.objects.filter(afiliado_id = afiliado, estado = True).exists()
        if estancias_activas:
            self.response_error['code'] = '0008'
            self.response_error['description'] = f'No puede anular el egreso de la estancia si existe otra activa para el paciente'
            return [True, self.response_error]

        return [False, self.response_error]

    
class EstanciaActivaRule2( ValidationRule ):
    '''         
        Se valida si la estancia se encuentra activa

        Parameters
        ----------
        estancia_id: integer
            Id de la estancia

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple
        '''
    
    def __init__(self, estancia_id):
        ValidationRule.__init__(self)
        self.estancia_id = estancia_id

   
    def validate(self):               
        estancia_inactiva =  EstanciaModel.objects.filter(id = self.estancia_id, estado = True).exists()
        if estancia_inactiva:
            self.response_error['code'] = '0009'
            self.response_error['description'] = 'La estancia se encuentra activa, no se puede realizar ninguna accion'
            self.validation = True

        return [self.validation, self.response_error]

class UltimaEstanciaRule( ValidationRule ):
    '''         
        Se valida si el id de estancia es diferente al ultimo id de estancia registrado para el paciente

        Parameters
        ----------
        estancia_id: integer
            Id de la estancia

        Returns
        -------
        validation: boolean
            True si existe la regla se cumple
        '''
    
    def __init__(self, estancia_id):
        ValidationRule.__init__(self)
        self.estancia_id = estancia_id

   
    def validate(self):               
        estancia = EstanciaModel.objects.filter(id = self.estancia_id).all().values()
        afiliado = estancia[0]['afiliado_id_id']
        ultima_estancia = EstanciaModel.objects.filter(afiliado_id = afiliado).values().last()
        if int(ultima_estancia['id']) != int(self.estancia_id):
            self.response_error['code'] = '0010'
            self.response_error['description'] = 'Solo puede ejecutar acciones sobre la ultima estancia reportada al paciente'
            self.validation = True

        return [self.validation, self.response_error]