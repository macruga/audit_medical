import os
import os.path as op
import numpy as np
import pandas as pd
import re
import datetime
import math

from abc import ABC, abstractmethod


class ValidationRule(ABC):
    '''
    Clase Abstracta para definir las diferentes reglas de validación de los campos en el sistema SIRIUS
    
    Attributes
    ----------
    value: list
        lista de valores que debe ser validados
        
    '''
    def __init__(self, nValues):
        ''' Crea un ValidationRule

        Método que instancia un objeto de la clase ValidationRule
        
        Parameters
        ----------
        nValue: list
            Lista de valores que se van a evaluar
        
        Raises
        ------
        ValueError
            Si la lista esta vacia 
        TypeError
            Si el parametro recibido no es de tipo lista
        
        '''
        if isinstance(nValues, list):
            if len(nValues) != 0:
                self.values = nValues
                super().__init__()
            else :
                raise ValueError('No se puede crear la regla de validación sobre una lista vacía')
        else:
            raise TypeError('El parametro no es de tipo lista')
        
    @abstractmethod
    def validate(self):
        pass
    
    
class NoCaracteresEspecialesValidationRule( ValidationRule ):
    '''Clase que valida que no se tengan caracteres especiales
    
    Clase que extiende a ValidationRule y revisa que los valores no tengan caracteres especiales del español 
    como tildes, eñes y vocales con dieresis
    '''
    _LISTA_CARACTERES_ESPECIALES = u'ÁÄÂÀÉËÊÈÍÏÎÌÓÖÔÒÚÜÛÙÑ'

    def __init__(self, nValues):
        ValidationRule.__init__(self, nValues)
    

    def hasSpecialChar(self, x):
        '''Indica si tiene un caracter especial del español

        Método que revisa que la cadena de caracteres x contenga alguno de los caracteres especiales del español

        Parameters
        ----------
        x:str
            cadena de caracters a revisar si tiene caracteres especiales del español
        
        Returns
        -------
        bool
            True si contiene caracteres especiales del español o False en caso contrario
        '''
        for y in self._LISTA_CARACTERES_ESPECIALES:
            if y in x:
                return True
        return False
        

    def validate(self):
        ''' Valida los caracteres especiales
        
        Método que valida que los elementos string del la lista de valores no contengan caracteres especiales del español

        Returns
        -------
        list
            Lista con un valor booleano indicando si tiene o no caracteres especiales por cada elemento de la lista de valores
        '''
        validos = [ ( str(x).replace(' ','').isalpha() and str(x).isupper() and not self.hasSpecialChar(x) ) if isinstance(x,str) else False for x in self.values]
        return validos
    
    

    
class TipoDeIdentificacionValidationRule( ValidationRule ):
    ''' Clase para validar el tipo de identificación
    
    Clase que revisa que los valores correspondan a los de la lista de tipos de documentos
    
    Attributes
    ----------
    tipos_documentos: list
        Lista con los tipos de documentos a revisar
    '''
    _TIPO_DOCUMENTOS = ['RC', 'TI', 'CC', 'CE', 'PA', 'MS', 'AS', 'CD', 'SC', 'PE']

    def __init__(self, values, listaDocumentos=[]):
        ''' Crea un TipoDeIdentificacionValidationRule

        Método que instancia un objeto de la clase TipoDeIdentificacionValidationRule
        
        Parameters
        ----------
        nValue: list
            Lista de valores que se van a evaluar
        listaDocumentos: list
            Lista con los tipos de documentos validos

        Raises
        ------
        ValueError
            Si la lista de valores esta vacia 
        TypeError
            Si el parametro de valores recibido no es de tipo lista
        '''
        ValidationRule.__init__(self, values)
        if len(listaDocumentos) == 0:
            self.tipos_documentos = self._TIPO_DOCUMENTOS
        else :
            self.tipos_documentos = listaDocumentos
    
    def validate(self):
        ''' Valida los tipos de docuento de identificación
        
        Método que valida que los elementos string del la lista de valores se encuentren en la lista de tipos de documentos validos

        Returns
        -------
        list
            Lista con un valor booleano indicando si el elemento de la lista de valores aparece o no en la lista de tipos de documento
        '''
        validos = [ (x in self.tipos_documentos) for x in self.values ]
        return validos
    
    
class FechaNacimientoValidationRule( ValidationRule ):
    '''Clase que revisa que la fecha de nacimiento sea valida

    Clase que permite validar si una fecha de nacimiento corresponde con una fecha de nacimiento valida, para lo cual establece que 
    la edad máxima para una persona es de 120 años, así una fecha de nacimiento valida es aquella que ocurrio hasta 120 años antes
    de la fecha actual
    '''
    def __init__(self, values):
        ValidationRule.__init__(self, values)
    
    def edadValida(self, x, edadMaxima = 120 ):
        ''' Valida la edad

        Metodo que valida que la edad sea mayor a cero y menor a la edad maxima

        Parameters
        ----------
        x: str
            Cadena de caracters con la fecha de nacimiento en formato YYYY-MM-DD
        edadMaxima: int
            Valor de edad máxima en años a considerar (120 años por defecto)
        
        Returns
        -------
        bool
            True si el valor de edad esta en el intervalo [0, edadMaxima]
        '''
        edad = int((pd.Timestamp('now') - pd.to_datetime(x)).days/365) 
        return True if edad >= 0 and edad <= edadMaxima else False 
    
    def validate(self):
        ''' Valida la fecha de nacimiento
        
        Método que valida que los elementos string del la lista de valores correspondan con fechas de nacimiento validas.
        Primero se valida que el formato corresponda a YYYY-MM-DD, luego se valida que la edad este en el rango especifico [0, edadMaxima]

        Returns
        -------
        list
            Lista con un valor booleano indicando si el elemento de la lista de valores corresponde a una fecha de nacimiento valida o no
        '''
        pattern = '^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'
        validos = [ ((True if re.match(pattern, str(x)) != None else False) and self.edadValida(x) )  for x in self.values ]
        return validos


class ValorEnListaValidationRule( ValidationRule ):
    '''Clase que revisa que los valores correspondan a los de la lista 

    Clase que permite validar que los valores de la lista a revisar se encuentren dentor de los valores contenidos en la lista de revisión
    
    Attributes
    ----------
    lista_revision: list
        Lista con los valores validos a revisar
    '''
    def __init__(self, values, listaRevision):
        '''Crea una instancia de ValorEnListaValidationRule

        Método constructor de la clase ValorEnListaValidationRule que instancia un objeto de la calse para la revisión de valores en la lista a revisar

        Parameters
        ----------
        values: list
            Lista de valores a revisar
        listaRevision: list
            Lista con los valores validos

        Raises
        ------
        ValueError
            Si la lista de valores validos esta vacia
        '''
        ValidationRule.__init__(self, values)
        if len(listaRevision) == 0:
            raise ValueError('ValueError:: La lista con valores válidos para revisión no puede ser vacía')
        else :
            self.lista_revision = listaRevision
    
    def validate(self):
        ''' Valida que los valores estén en la lista 
        
        Método que valida que los elementos del la lista de valores correspondan con alguno de los elemntos de la lista de valores válidos
        
        Returns
        -------
        list
            Lista con un valor booleano indicando si el elemento de la lista de valores esta en la lista de elemntos validos o no
        '''
        validos = [ (x in self.lista_revision) for x in self.values ]
        return validos


class NumeroTelefonicoValidationRule(ValidationRule):
    '''Clase para revisar la validez de un número telefónico

    Clase que permite evaluar si los números telefónicos tienen un formato valido, 
    
    Attributes
    ----------
    _max_phone_numbers: int
        indica el maximo numero de telefonos posibles en un elemento de la lista
    _sep: str
        Indica el separador válido de números telefónicos en el elemento
    '''
    def __init__(self, values, maxPhoneNumbers=2, separator='-'):
        ''' Crea una instancia de NumeroTelefonicoValidationRule

        Crea una instancia de la clase NumeroTelefonicoValidationRule, indicando el número máximo de teléfonos permitidos así como el separador para identificarlos

        Parameters
        ----------
        values: list
            Lista de valores a revisar si el teléfono es válido
        maxPhoneNumbers: int
            Indica el número máximo de números telefónicos a considerar, por defecto 2
        separator: str
            Indica el separador a utilizar entre un número télefonico y otro
        '''
        ValidationRule.__init__(self, values)
        self._max_phone_numbers = maxPhoneNumbers
        self._sep=separator

    def esNumeroValido(self, x):
        '''Valida que el elemento x contenga número(s) telefónico(s) válido(s)

        Valida al contenido de x para indoicar si tiene uno o mas números telefónicos validos, no puede tener mas números que el establecido en max_phone_number y 
        deben estar separados por el caracter delimitador

        Parameters
        ----------
        x: str
            Cadena de caracteres que contiene el(los) número(s) telefónico(s)
        
        Returns
        -------
        bool
            True si el contenido es valido o False en caso contrario

        '''
        pattern = '^(\d{5,})'
        valido = True
        xx = x.split(self._sep)
        if len(xx) <= self._max_phone_numbers :
            for xn in xx:
                if re.match(pattern, xn.strip()) == None :
                    valido = False
        else:
            valido = False
        return valido
    
    def validate(self):
        ''' Valida que los valores sean números telefónicos 
        
        Método que valida que los elementos del la lista de valores correspondan a números telefónicos
        
        Returns
        -------
        list
            Lista con un valor booleano indicando si el elemento de la lista de valores contiene números telefónicos validos o no
        '''
        validos = [(self.esNumeroValido(x) or str(x) == '0') for x in self.values]

        return validos


class FechaValidationRule(ValidationRule):
    '''Clase para revisar la validez de una Fecha

    Clase que permite evaluar si las fechas son validas, se espera que las fechas esten en formato YYYY-MM-DD, y no sean menores 
    a la fecha actual menos el valor de umbral. También se considera que la fecha tenga un valor por defecto indicado en la lista 
    de fechas por defecto
    
    Attributes
    ----------
    _fechas_por_defecto: list
        lista con las opciones de fecha por defecto validas
    _umbral_valido: int
        Indica el numero de años que definen el rango válido de fechas
    '''
    def __init__(self, values, opcionesPorDefecto=[], umbralValido=5):
        '''Crea un objeto de la clase FechaValidationRule

        Crea ina instancia de la clase FechaValidationRule para validar que las fechas sean correctas, uns fecha correcta esta en formato 
        YYYY-MM-DD y tiene un valor en el intervalo [hoy-umbral,  hoy], es decir es valida si no es mayor a hoy y si no es menor a hoy 
        menos el umbral (que es en años)

        Parameters
        ----------
        opcionesPorDefecto: list
            Lista con las opciones de fecha por defecto a considerar como valores válidos aún si están fuera del rango
        umbralValido:int
            Número de años a considerar en la definición del intervalo de fechas valido, por defecto cinco (5)

        '''
        ValidationRule.__init__(self, values)
        self._fechas_por_defecto = opcionesPorDefecto
        self._umbral_valido = umbralValido
    
    def esFechaValida(self, x ):
        '''Indica si la fecha es valida
        Indica si la fecha en el paramétro x corresponde a una fecha válida

        Parameters
        ----------
        x: str
            Fecha a revisar
        '''
        try:
            edad = math.floor((pd.Timestamp('now') - pd.to_datetime(str(x),errors='coerce')).days/365)
        except :
            edad = self._umbral_valido*10
            
        return True if edad <= self._umbral_valido and edad >= 0 else False 
        
    def validate(self):
        '''Valida que los valores sean fechas correctas 
        
        Método que valida que los elementos del la lista de valores correspondan a fechas correctas
        
        Returns
        -------
        list
            Lista con un valor booleano indicando si el elemento de la lista de valores contiene una fecha valida o no
        '''
        pattern = '^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$'
        validos = [ (((True if re.match(pattern, str(x)) != None else False) and self.esFechaValida(x)) or (x in self._fechas_por_defecto))  for x in self.values ]
        return validos


class CodigoCIEValidationRule(ValidationRule):
    ''' Clase que revisa los valores de CIE10
    Clase que revisa que los valores del codigo sean de cuatro digitos e incien por letra y los 
    demás sean númericos, además puede revisar que este en un listado actualizado de códigos CIE
    
    Attributes
    ----------
    opciones_defecto: list
        Lista con los códigos cie 10 a validar

    '''
    def __init__(self, values, opcionesXDefecto=[]):
        '''Crea una instancia de la clase CodigoCIEValidationRule

        Crea la instancia de la clase CodigoCIEValidationRule para la validación del codigo CIE-10,

        Parameters
        ----------
        opcionesXDefecto: list
            Lista de codigos que deben ser validados como correctos
        '''
        ValidationRule.__init__(self, values)
        self.opciones_defecto = opcionesXDefecto
        
    def estaEnListaXDefecto(self, x):
        '''indica si esta en la lista por defecto

        Método que revisa si el valor x esta en la lista de valores por defecto, si la lista por 
        defecto esta vacia retorna True

        Parameters
        ----------
        x: str
            Valor a revisar si esta en la lista

        Returns
        -------
        bool
            True si esta en la lista o False en caso contrario
        '''
        return True if x in self.opciones_defecto else False
    
    def validar_formato_cie(self, x):
        '''Valida que tenga el formato de codigos CIE-10

        Método que valida que el parámetro x cumple el formato de códigos CIE-10

        Parameters
        ----------
        x: str
            Valor a revisar si esta en la lista

        Returns
        -------
        bool
            True si esta en la lista o False en caso contrario
        '''
        if isinstance(x, str):
            return (len(x) == 4) and ((x[0].isupper()) and (x[0].isalpha())) and (x[1:].isdigit() or (x[1:3].isdigit() and x[3].isalpha()))
        return False
    
    def validate(self):
        '''Valida que los valores sean códigos CIE-10
        
        Método que valida que los elementos del la lista de valores correspondan a códigos del diccionario CIE-10
        
        Returns
        -------
        list
            Lista con un valor booleano indicando si el elemento de la lista de valores contiene un código CIE-10 o no
        '''
        if len(self.opciones_defecto) != 0:
            validos = [(self.validar_formato_cie(x) or self.por_defecto(x)) for x in self.values ]
        else: 
            validos = [self.validar_formato_cie(x) for x in self.values ]
        return validos


class NumeroValidationRule( ValidationRule ):
    '''Clase para validar valores numéricos

    Clase que permite validar que los valores son de tipo numérico o están en als opciones por defecto

    Attributes
    ----------
    opciones_defecto: list
        Lista con los valores por defecto adicionales al valor numérico
    '''
    def __init__(self, values, opcionesXDefecto=[]):
        '''Crea una instancia de la calse NumeroValidationRule

        Crea una instancia de la clase NumeroValidationRule para revisar que los campos sean de tipo numérico
        o pertenzcan a la lista de valores por defecto

        Parameters
        ----------
        opcionesXDefecto: list
            Lista de valores a considerar como valores por defecto adicional al valor númerico
        '''
        ValidationRule.__init__(self, values)
        self.opciones_defecto = opcionesXDefecto
    
    def validate(self):
        '''Valida que los valores sean numéricos
        
        Método que valida que los elementos del la lista de valores correspondan a valores numéricos
        
        Returns
        -------
        list
            Lista con un valor booleano indicando si el elemento de la lista de valores es numérico o no
        '''
        if len(self.opciones_defecto) == 0:
            validos = [ str(x).isdigit() for x in self.values ]
        else:
            validos = [((str(x).isdigit()) or (x in self.opciones_defecto)) for x in self.values ]
        return validos


class FechaExactaValidationRule(ValidationRule):
    '''Clase para validar una fecha exacta

    Clase que permite validar una fecha exacta para un campo

    Attributes
    ----------
    fecha_exacta: date
        La fecha que se requiere validar
    '''
    def __init__(self, values, fecha):
        '''Crea una instancia de FechaExactaValidationRule

        Crea una instancia de la clase FechaExactaValidationRule para validar una fecha específica en los campos

        Parameters
        ----------
        fecha: Date
            Fecha que se quiere validar
        '''
        ValidationRule.__init__(self, values)
        self.fecha_exacta = fecha
    
    def validate(self):
        '''Valida que los valores correspondan a la fecha
        
        Método que valida que los elementos del la lista de valores correspondan exactamente a la fecha indicada.
        
        Returns
        -------
        list
            Lista con un valor booleano indicando si el elemento de la lista de valores corresponde a la fecha o no
        '''
        # TODO: revisar si requiere convertir el formato de la fecha antes de la comparación
        validos = [True if x == self.fecha_exacta else False for x in self.values]
        return validos
    

class NumeroDocumentoValidationRule( ValidationRule ):
    '''Clase para validar un numero de documento

    Clase que permite validar que el contenido del campo corresonda a un número de identificación correcto
    '''
    def __init__(self, values):
        ValidationRule.__init__(self, values)
        
    def hasSpecialChar(self, x):
        '''Indica si tienen un caracter especial

        Método que indica si el valor x contiene algún caracter especial

        Returns
        -------
        bool
            True si contiene algún caracter especial o False en caso contrario 
        '''
        listaCaracteresEspeciales = 'ÁÄÂÀÉËÊÈÍÏÎÌÓÖÔÒÚÜÛÙÑ.'
        for y in listaCaracteresEspeciales:
            if y in str(x):
                return True
        return False
    
    def validate(self):
        '''Valida que los valores correspondan a números de documento
        
        Método que valida que los elementos del la lista de valores correspondan a números de documento.
        
        Returns
        -------
        list
            Lista con un valor booleano indicando si el elemento de la lista de valores corresponde a un número de documento o no
        '''
        validos = [(str(x).isalnum() and not self.hasSpecialChar(x)) for x in self.values]
        return validos


class CodigoMunicipioValidationRule( ValidationRule ): 
    '''Clase para validar el código de municipio

    Clase que permite validar el código de municipio, el cual es numérico de 5 digitos 

    Attributes
    ----------
    codigos_municipios: lista
        Lista con los códigos de municipio válidos
    '''
    def __init__(self, values, codigosMunicipios):
        '''Crea una CodigoMunicipioValidationRule

        Crea una instancia de la clase CodigoMunicipioValidationRule para validar los códigos de municipio,
        un código de municipio es numérico de 5 dígitos con ceros a la izquierda de necesitarse y debe 
        aparecer en la lista de códigos de municipio

        Parameters
        ----------
        codigosMunicipios: list
            Lista con los códigos de municipio validos
        '''
        ValidationRule.__init__(self, values)
        self.codigos_municipios = codigosMunicipios
    
    def validate(self):
        '''Valida que los valores correspondan a códigos de municipio
        
        Método que valida que los elementos del la lista de valores correspondan a códigos de municipio
        
        Returns
        -------
        list
            Lista con un valor booleano indicando si el elemento de la lista de valores corresponde a un código de municipio o no
        '''
        validos = [(len(str(x)) == 5 and x in self.codigos_municipios ) for x in self.values]
        return validos


class ValorEnListaOpcionDefectoValidationRule( ValidationRule ):
    '''
    Clase que revisa que los valores correspondan a los de la lista
    
    Attributes
    ----------
    lista_revision: list
        Lista con los valores validos a revisar
    opcion_defecto: list
        Lista con los valores por defecto validos
    '''
    def __init__(self, values, listaRevision, opcionDefecto):
        '''Crea una ValorEnListaOpcionDefectoValidationRule

        Crea un objeto de tipo ValorEnListaOpcionDefectoValidationRule para validar que el elemento esta 
        en la lista de valores válidos o corresponde a una opción por defecto

        Parameters
        ----------
        listaRevision: list
            Lista con los valores válidos 
        opcionDefecto: list
            Lista con las opciones por defecto

        Raises
        ------
        ValueError
            Si cualquiera de las listas, de opciones validas o de valores por defecto, está vacía
        '''
        ValidationRule.__init__(self, values)
        if len(listaRevision) == 0:
            raise ValueError('ValueError:: La lista para validacion no puede ser vacia')
        elif len(opcionDefecto) == 0:
            raise ValueError('ValueError:: La lista por defecto no puede ser vacia')
        else :
            self.lista_revision = listaRevision
            self.opcion_defecto = opcionDefecto
    
    def validate(self):
        '''Valida que los valores correspondan a valores en la lista
        
        Método que valida que los elementos del la lista de valores correspondan a valores en la lista de validación 
        
        Returns
        -------
        list
            Lista con un valor booleano indicando si el elemento de la lista de valores es en al lista de válidos o no
        '''
        validos = [ ((x in self.lista_revision) or (x in self.opcion_defecto)) for x in self.values ]
        return validos    


class DummyValidationRule( ValidationRule ):
    ''' Clase que retorna True como validacion de campos

    Clase que retorna True a cada valor a revisar
    '''
    def __init__(self, values):
        ValidationRule.__init__(self, values)
    def validate(self):
        validos = [ True for x in self.values ]
        return validos

