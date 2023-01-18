import pandas as pd
import numpy as np
from django.conf import settings
import os

from core.tools.databases.mssql_azure import MssqlAzure
from core.FieldsValidator import *

from censo.models.censo import censoModel

class fieldsValidation():
    '''Clase para validacion de archivos de censo cargados

    Clase que permite validar al consistencia y coherencia de la información cargada a través de la aplicación de censo.
    La clase permite revisar la validez de cada uno de los campos aspi como la coherencia de los valores entre los mismos para un registro de Censo

    Attributes
    ----------
    file: str
        Archivo cargado en el storage de SMD
    dataCenso: pandas.DataFrame
        Data frame con la información cargada para ser validada.
    dbEngine: MssqlAzure
        Motor de conexión a la base de datos
    '''
    # init method or constructor
    def __init__(self, file, type):
        self.file = file
        # print(self.file)

        if type in ['XLS','XLSX']:
            self.dataCenso = pd.read_excel(os.path.join(settings.MEDIA_ROOT, file))
            # print(">>> :D",self.file)
        else:
            self.dataCenso = pd.read_csv(os.path.join(settings.MEDIA_ROOT, file), sep=";")
            # print(">>> :P",self.file)
        # dtype={'Day': str,'Wind':int64}
        self.dataCenso = self.dataCenso.dropna(subset=['Fecha Ingreso', 'Dx Ingreso'])
        self.dataCenso['Código habilitación IPS'] = self.dataCenso['Código habilitación IPS'].astype(int)
        self.dataCenso['Código habilitación IPS'] = self.dataCenso['Código habilitación IPS'].astype(str)
        self.dataCenso['Código habilitación IPS'] = self.dataCenso['Código habilitación IPS'].apply(lambda x: '{0:0>12}'.format(x))
        self.dataCenso['Núm. Identificación'] = self.dataCenso['Núm. Identificación'].astype(np.int64)

        # print(self.dataCenso)

        self.dbEngine = MssqlAzure(echo=False)
        query = "select name FROM sys.databases;"
        data = pd.read_sql(query, self.dbEngine.engine)
        print(data)


    def __obtenerListaIPS(self):
#        # bdConn = MssqlAzure(server=host, user=username, pwd=password, db=db, port=portdb, echo=False)
#        bdConn = MssqlAzure(echo=False)
#        # query = "select name FROM sys.databases;"
#        # data = pd.read_sql(query, bdConn.engine)
        query = "select * FROM core_ipsmodel"
        data = pd.read_sql(query, self.dbEngine.engine)
        # print(data.shape)
        return data['codigo_habilitacion'].to_list()

    def __obtenerListaCIE10(self):
#        bdConn = MssqlAzure(echo=False)
        query = "select * FROM core_cie10model"
        data = pd.read_sql(query, self.dbEngine.engine)
        # print(data.shape)
        return data['codigo'].to_list()

    def __obtenerListaTiposDocumento(self):
        query = "select * FROM core_tipodocumentomodel"
        data = pd.read_sql(query, self.dbEngine.engine)
        # print(data.shape)
        return data['codigo'].to_list()

    def __obtenerTiposIngreso(self):
        query = "select * FROM censo_tipoingresomodel"
        data = pd.read_sql(query, self.dbEngine.engine)
        data = data[data['active']==True][['id', 'description']]
        # print(data.shape)
        return data

    def __obtenerOrigenesEvento(self):
        query = "select * FROM censo_origeneventomodel"
        data = pd.read_sql(query, self.dbEngine.engine)
        data = data[data['active']==True][['id', 'description']]
        # print(data.shape)
        return data

    def __obtenerTiposHabitacion(self):
        query = "select * FROM censo_tipohabitacionmodel"
        data = pd.read_sql(query, self.dbEngine.engine)
        data = data[data['active']==True][['id', 'description']]
        # print(data.shape)
        return data

    def __obtenerCondicionesEgreso(self):
        query = "select * FROM censo_condicionaltacensomodel"
        data = pd.read_sql(query, self.dbEngine.engine)
        data = data[data['active']==True][['id', 'description']]
        # print(data.shape)
        return data
        

    def __darAfiliado(self, tipoDoc, numDoc):
        query =  "Select * FROM afiliados_afiliadomodel WHERE tipo_identificacion = '"+tipoDoc+"' AND identificacion = '"+str(numDoc)+"'" 

        dataAf = pd.read_sql(query, self.dbEngine.engine)
        if dataAf.shape[0] == 0:
            # buscar solo por el numero de documento
            query =  "Select * FROM afiliados_afiliadomodel WHERE identificacion = '"+str(numDoc)+"'" 
            dataAf = pd.read_sql(query, self.dbEngine.engine)

        if dataAf.shape[0] > 0:
            return dataAf
            # TODO: Review multiple records
            afiliado_id = dataAf.at[0,'id']
            # print("ID AFILIADO:", afiliado_id)
            query =  "Select * FROM afiliados_afiliacionmodel WHERE afiliado_id = "+str(afiliado_id)
            data = pd.read_sql(query, self.dbEngine.engine)
            if data.shape[0] > 0:
                # print(data.shape)
                # TODO: revisar si hay mas de una afiliación cual devuelve. 
                return [data, dataAf]
            else :
                # TODO Crear el tipo específico de excepción
                raise Exception("No hay datos de la afiliación")
        else:
            # TODO Crear el tipo específico de excepción
            raise Exception("No hay datos del afiliado")

    def __darUltimoCenso(self, tipo_doc, num_doc):
        censoPaciente = pd.DataFrame.from_records(censoModel.objects.filter(tipo_identificacion_id=tipo_doc, identificacion=num_doc).values(
            'id', 'fecha_ingreso', 'tipo_identificacion_id', 'identificacion', 'dx_ingreso', 'tipo_ingreso_id', 'origen_evento_id', 'dx_actual', 
             'tipo_habitacion_id', 'codigo_ips_id', 'fecha_egreso', 'condicion_alta_id', 'dx_egreso', 'fecha_censo', 'dias_estancia', 'reingreso', 
             'afiliado_id',  'created', 'owner_id', 'active'))
        if censoPaciente.shape[0] > 0:
            censoPaciente = censoPaciente.sort_values(by="fecha_censo", ascending=False)
        return censoPaciente

    def __calcularEdad(self, fecha_nacimiento, verbose=False):
        born = pd.to_datetime(fecha_nacimiento)
        today = pd.to_datetime('today')
        if verbose: print(f" Born was: {born} and today is: {today}")
        age = today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        return age       

    def validate(self, verbose=True):
        # Remove rows with NAN Values in DxIngreso and Fecha Ingreso
        # data = self.dataCenso.dropna(subset=['Fecha Ingreso', 'Dx Ingreso'])
        data = self.dataCenso.copy()
        # para cada fila en el dataframe revisar las reglas
        if verbose : print("Iniciando Validación para ",data.shape[0], "registros")
        cols = list(data.columns)
        cols.append('Error')

        dfValidos = pd.DataFrame(columns=self.dataCenso.columns)
        dfNoCumple = pd.DataFrame(columns=cols)
        
        # TODO: Obtener la duración para considerar reingreso desde algún servicio
        dias_reingreso = 10

        if verbose :
            print("Columnas Validos", dfValidos.columns)
            print("Columnas Invalidos", dfNoCumple.columns)

        # listas de opciones
        # tipos_de_documento = ['MS', 'RC', 'TI', 'CC', 'CE', 'PA', 'UN', 'NT', 'AS', 'CD', 'CN', 'SC', 'PE']
        # tipos_de_ingreso = ['URGENCIAS', 'REMITIDO', 'PROGRAMADO', 'REINGRESO ANTES DE LOS 15 DIAS']
        # origenes_de_evento = ['ENFERMEDAD GENERAL', 'ATEP', 'SOAT', 'TUTELA']
        # tipos_de_habitacion = ['ESTANCIA EN BASICO', 'OBSERVACION URGENCIAS', 'CUIDADO INTERMEDIO', 'UCI ADULTO', 'UCI NEONATAL', 'UCI PEDIATRICA']
        # condiciones_de_alta = ['Continua Tratamiento_Corte de Cuenta', 'Defunción antes de 48 horas general', 'Defunción antes de 48 horas materna', 'Defunción antes de 48 horas perinatal', 
        #                        'Defunción despúes de 48 horas general', 'Defunción despúes de 48 horas materna', 'Defunción despúes de 48 horas perinatal', 'Mejora', 'PHD agudo', 
        #                        'PHD Crónico', 'Salida voluntaria', 'Traslado', 'Fuga del paciente']
        tipos_de_documento = self.__obtenerListaTiposDocumento()
        dfTiposDeIngreso = self.__obtenerTiposIngreso()
        dfOrigenesEvento = self.__obtenerOrigenesEvento()
        dfTiposHabitacion = self.__obtenerTiposHabitacion()
        dfCondicionesAlta = self.__obtenerCondicionesEgreso()

        # Traer los codigos CIE10
        codigosCIE10 = self.__obtenerListaCIE10()
        # Traer los códigos de las IPS
        codigosIPS = self.__obtenerListaIPS()
        
        # Revisar que en la base cargada no hayan duplicados, si los hay dejarlos aparte
        dfDuplicados = data[data.duplicated(subset=['Tipo Identificación','Núm. Identificación','Fecha Censo','Código habilitación IPS'])]
        
        # for i in tqdm.tqdm(range(0, dfX.shape[0])):
        for i in range(0, data.shape[0]):
            if not (data.iloc[i].isna()).all() :
                errores = []
                dfY = data.iloc[i]
                if verbose: print(i, dfY)

                # validar campos independientes
                fecha_ingreso = dfY['Fecha Ingreso']
                fecha_censo = dfY['Fecha Censo']
                fecha_egreso = dfY['Fecha Egreso']

                dx_actual = dfY['Dx Actual']

                tipo_doc = dfY['Tipo Identificación']
                num_doc = dfY['Núm. Identificación']

                # Validar registro duplicado en la base cargada
                dfDuplicadosCarga = dfDuplicados[
                    (dfDuplicados['Tipo Identificación'] == tipo_doc) &
                    (dfDuplicados['Núm. Identificación'] == num_doc) &
                    (dfDuplicados['Fecha Censo'] == fecha_censo) &
                    (dfDuplicados['Código habilitación IPS'] == dfY['Código habilitación IPS'])
                ]
                if dfDuplicadosCarga.shape[0] > 0:
                    if verbose: print("Duplicado")
                    errores.append({'Duplicado' : 'Existe otro registro para el mismo paciente en el mismo día dentro del archivo'})

                # afiliacion = pd.DataFrame()
                afiliado = pd.DataFrame()
                try:
                    # afiliacion, afiliado = self.__darAfiliado(tipo_doc, num_doc)
                    afiliado = self.__darAfiliado(tipo_doc, num_doc)
                    # if verbose: print(afiliacion, afiliado)
                    if verbose: print(afiliado)
                    
                    edad = self.__calcularEdad(afiliado.iloc[0]['fecha_nacimiento'], verbose=True)
                    if edad > 120:
                        errores.append({'Edad': edad, 'Error' : 'Edad superior a 120 años'})
                    elif edad == 0:
                        if not tipo_doc in(['MS', 'RC']) :
                            errores.append({'Edad': edad, 'Tipo Identificación': tipo_doc, 'Error' : 'Coherencia entre edad y tipo de documento de identificación'})
                    # if edad >= 14 and not dfY['Tipo Habitación'] in ['ESTANCIA EN BASICO', 'OBSERVACION URGENCIAS', 'CUIDADO INTERMEDIO', 'UCI ADULTO']:
                    #     errores.append({'Edad' : edad, 'Tipo Habitación': dfY['Tipo Habitación'], 'Error' : 'Coherencia entre tipo de habitación y edad'})
                    # else :
                    #     if edad == 0: 
                    #         dias = (pd.to_datetime('Today') - pd.to_datetime(afiliado.iloc[0]['fecha_nacimiento'])).days
                    #         if dias <= 30 and not dfY['Tipo Habitación'] in ['ESTANCIA EN BASICO', 'OBSERVACION URGENCIAS', 'CUIDADO INTERMEDIO', 'UCI NEONATAL'] :
                    #             errores.append({'Edad' : edad, 'Tipo Habitación': dfY['Tipo Habitación'], 'Error' : 'Coherencia entre tipo de habitación y edad menor a 30 días'})
                    #         elif not dfY['Tipo Habitación'] in ['ESTANCIA EN BASICO', 'OBSERVACION URGENCIAS', 'CUIDADO INTERMEDIO', 'UCI PEDIATRICA']:
                    #             errores.append({'Edad' : edad, 'Tipo Habitación': dfY['Tipo Habitación'], 'Error' : 'Coherencia entre tipo de habitación y edad mayor a 30 días'})
                    #     if edad != 0 and not dfY['Tipo Habitación'] in ['ESTANCIA EN BASICO', 'OBSERVACION URGENCIAS', 'CUIDADO INTERMEDIO', 'UCI PEDIATRICA']:
                    #         errores.append({'Edad' : edad, 'Tipo Habitación': dfY['Tipo Habitación'], 'Error' : 'Coherencia entre tipo de habitación y edad_'})

                except Exception as exp:
                    if verbose: print(exp)
                    errores.append({'Afiliacion': tipo_doc+str(num_doc), 'Error' : 'Afiliación No existente'})

                try:
                    validadorFecha = FechaValidationRule([fecha_ingreso])
                    if not validadorFecha.validate()[0] :
                        errores.append({'Fecha Ingreso' : fecha_ingreso, 'Error': 'Fecha Invalida'}) 
                except:
                    errores.append({'Fecha Ingreso' : fecha_ingreso, 'Error': 'Formato de fecha Invalido'}) 

                try:
                    validation = TipoDeIdentificacionValidationRule([dfY['Tipo Identificación']], tipos_de_documento)
                    if not validation.validate()[0] :
                        errores.append({'Tipo Identificación' : dfY['Tipo Identificación'], 'Error': 'Tipo Identificación Invalido'}) 
                except:
                    errores.append({'Tipo Identificación' : dfY['Tipo Identificación'], 'Error': 'Formato de Tipo Identificación Invalido'})

                try:
                    validation = NumeroDocumentoValidationRule([dfY['Núm. Identificación']])
                    if not validation.validate()[0] :
                        errores.append({'Núm. Identificación' : dfY['Núm. Identificación'], 'Error': 'Número de Identificación Invalido'}) 
                except:
                    errores.append({'Núm. Identificación' : dfY['Núm. Identificación'], 'Error': 'Formato de Número de Identificación Invalido'})

                try:
                    validation = CodigoCIEValidationRule([dfY['Dx Ingreso']], codigosCIE10)
                    if not validation.validate()[0] :
                        errores.append({'Dx Ingreso' : dfY['Dx Ingreso'], 'Error': 'Diagnóstico de Ingreso Invalido'}) 
                except:
                    errores.append({'Dx Ingreso' : dfY['Dx Ingreso'], 'Error': 'Formato de Diagnóstico de Ingreso Invalido'})
                
                try:
                    validation = ValorEnListaValidationRule([dfY['Tipo Ingreso']], dfTiposDeIngreso['description'].to_list())
                    if not validation.validate()[0] :
                        errores.append({'Tipo Ingreso' : dfY['Tipo Ingreso'], 'Error': 'Tipo Ingreso Invalido'}) 
                except:
                    errores.append({'Tipo Ingreso' : dfY['Tipo Ingreso'], 'Error': 'Formato de Tipo Ingreso Invalido'})

                try:
                    validation = ValorEnListaValidationRule([dfY['Origen Evento']], dfOrigenesEvento['description'].to_list())
                    if not validation.validate()[0] :
                        errores.append({'Origen Evento' : dfY['Origen Evento'], 'Error': 'Origen Evento Invalido'}) 
                except:
                    errores.append({'Origen Evento' : dfY['Origen Evento'], 'Error': 'Formato de Origen Evento Invalido'})
                
                try:
                    validation = CodigoCIEValidationRule([dx_actual], codigosCIE10)
                    if not validation.validate()[0] :
                        errores.append({'Dx Actual' : dx_actual, 'Error': 'Diagnóstico Actual Invalido'}) 
                except:
                    errores.append({'Dx Actual' : dx_actual, 'Error': 'Formato de Diagnóstico Actual Invalido'})

                try:
                    validation = ValorEnListaValidationRule([dfY['Tipo Habitación']], dfTiposHabitacion['description'].to_list())
                    if not validation.validate()[0] :
                        errores.append({'Tipo Habitación' : dfY['Tipo Habitación'], 'Error': 'Tipo Habitación Invalido'}) 
                except:
                    errores.append({'Tipo Habitación' : dfY['Tipo Habitación'], 'Error': 'Formato de Tipo Habitación Invalido'})

                try:
                    validation = ValorEnListaValidationRule([dfY['Código habilitación IPS']], codigosIPS)
                    if not validation.validate()[0] :
                        errores.append({'Código habilitación IPS' : dfY['Código habilitación IPS'], 'Error': 'Código habilitación IPS Invalido'}) 
                except:
                    errores.append({'Código habilitación IPS' : dfY['Código habilitación IPS'], 'Error': 'Formato de Código habilitación IPS Invalido'})

                try:
                    validadorFecha = FechaValidationRule([fecha_censo])
                    if not validadorFecha.validate()[0] :
                        errores.append({'Fecha Censo' : fecha_censo, 'Error': 'Fecha Censo Invalida'}) 
                except:
                    errores.append({'Fecha Censo' : fecha_censo, 'Error': 'Formato de Fecha Censo Invalido'})

                try: 
                    # Los campos opcionales mientras se produce un ingreso
                    if not (dfY[['Condición de alta', 'Dx Egreso', 'Fecha Egreso']].isna()).all() :
                        try:
                            validadorFecha = FechaValidationRule([fecha_egreso])
                            if not validadorFecha.validate()[0] :
                                errores.append({'Fecha Egreso' : fecha_egreso, 'Error': 'Fecha Egreso Invalida'}) 
                        except:
                            errores.append({'Fecha Egreso' : fecha_egreso, 'Error': 'Formato de Fecha Egreso Invalido'}) 

                        try:
                            validation = ValorEnListaValidationRule([dfY['Condición de alta']], dfCondicionesAlta['description'].to_list())
                            if not validation.validate()[0] :
                                errores.append({'Condición de alta' : dfY['Condición de alta'], 'Error': 'Condición de alta Invalida'}) 
                        except:
                            errores.append({'Condición de alta' : dfY['Condición de alta'], 'Error': 'Formato de Condición de alta Invalido'})
                        
                        try:
                            validation = CodigoCIEValidationRule([dfY['Dx Egreso']], codigosCIE10)
                            if not validation.validate()[0] :
                                errores.append({'Dx Egreso' : dfY['Dx Egreso'], 'Error': 'Diagnóstico Egreso Invalido'}) 
                        except:
                            errores.append({'Dx Egreso' : dfY['Dx Egreso'], 'Error': 'Formato de Diagnóstico de egreso Invalido'})
                    # elif not (dfY[['Condición de alta', 'Dx Egreso', 'Fecha Egreso']].isna()).any() : 
                    #     errores.append({'Egreso': dfY['Dx Egreso'], 'Error':'Faltan datos en alguno(s) de los tres campos del egreso del paciente del censo'})
                except Exception as exp: 
                    if verbose: print(exp)
                    pass
                
                # Validar secuencia de fechas
                if pd.to_datetime(fecha_ingreso) > pd.to_datetime(fecha_censo) :
                    errores.append({'Fecha Ingreso' : fecha_ingreso, 'Fecha Censo': fecha_censo, 'Error': 'Fecha de Censo anterior a la fecha de ingreso'})

                try:
                    # if np.isnan(dfY['Fecha Egreso']):
                    if pd.isna(dfY['Fecha Egreso']):
                        if pd.to_datetime(fecha_ingreso) > pd.to_datetime(fecha_egreso) :
                            errores.append({'Fecha Ingreso' : fecha_ingreso, 'Fecha Egreso': fecha_egreso, 'Error': 'Fecha de egreso anterior a la fecha de ingreso'})
                        if pd.to_datetime(fecha_censo) > pd.to_datetime(fecha_egreso) :
                            errores.append({'Fecha Censo' : fecha_censo, 'Fecha Egreso': fecha_egreso, 'Error': 'Fecha de egreso anterior a la fecha de Censo'})
                except Exception as exp: 
                    if verbose: print(exp)
                    pass

                # Calcular dias de estancia
                dias_estancia = pd.to_datetime(fecha_censo) - pd.to_datetime(fecha_ingreso)
                if verbose: print("Dias estancia", type(dias_estancia), dias_estancia, dias_estancia.days + 1)
                dfY['dias_estancia'] = dias_estancia.days + 1

                # TODO
                # if dias_estancia.days >= 3 and dx_actual[0] in ['R', 'Z'] :
                #     errores.append({'Dx Actual' : dx_actual, 'Días estancia': dias_estancia, 'Error': 'el diaǵnostico no puede ser sindromático a partir del 3er día'})

                # Obtener el último censo del paciente en la base de censo
                dfCensoPaciente = self.__darUltimoCenso(tipo_doc, num_doc)
               
                # 1 - Nunca ha tenido censo (Nuevo)
                if dfCensoPaciente.shape[0] == 0: 
                    dfY['reingreso'] = False
                
                # 2 - Ha tenido censo 
                else:
                    print("Ha tenido Censo")
                    print(dfCensoPaciente[['fecha_ingreso', 'fecha_censo', 'tipo_identificacion_id', 'identificacion']])
                    if verbose:
                        print(type(dfCensoPaciente), dfCensoPaciente.columns, dfCensoPaciente.iloc[0], type(dfCensoPaciente.iloc[0]))
                        print("VALUE::",dfCensoPaciente.iloc[0]['fecha_egreso'])
                    print(fecha_ingreso, fecha_censo)
                    print(
                        dfCensoPaciente[
                            (pd.to_datetime(dfCensoPaciente['fecha_ingreso'])==pd.to_datetime(fecha_ingreso))
                            & (pd.to_datetime(dfCensoPaciente['fecha_censo'])==pd.to_datetime(fecha_censo))
                            & (str(dfCensoPaciente['identificacion'])==str(dfY['Núm. Identificación']))
                        # & (dfCensoPaciente['tipo_identificacion_id']==dfY['Tipo Identificación'])
                        ]
                    )
                    # 2.0 revisar que no exista un registro igual en el censo, es decir para un paciente el mismo dia de ingreso y de censo
                    dfCensoPacienteDuplicado = dfCensoPaciente[
                        (pd.to_datetime(dfCensoPaciente['fecha_ingreso'])==pd.to_datetime(fecha_ingreso))
                        & (pd.to_datetime(dfCensoPaciente['fecha_censo'])==pd.to_datetime(fecha_censo))
                    ]
                    if dfCensoPacienteDuplicado.shape[0] > 0:
                        if verbose:
                            print("Censo Duplicado en sistema", dfCensoPacienteDuplicado.iloc[0][['fecha_ingreso', 'fecha_censo', 'tipo_identificacion_id', 'identificacion']])
                        errores.append({
                            'fecha Censo': dfCensoPacienteDuplicado.iloc[0]['fecha_censo'],
                            'Tipo Documento': dfCensoPacienteDuplicado.iloc[0]['tipo_identificacion_id'],
                            'Identificacion': dfCensoPacienteDuplicado.iloc[0]['identificacion'],
                            'Fecha Ingreso' : dfCensoPacienteDuplicado.iloc[0]['fecha_ingreso'],
                            'Error': 'Censo duplicado en el sistema'})

                    # 2.1 - Esta abierto - que no tiene fecha de egreso
                    if dfCensoPaciente.iloc[0]['fecha_egreso'] == None :
                        # 2.1.1 - Validar que la fecha de ingreso sea la misma
                        if pd.to_datetime(dfCensoPaciente.iloc[0]['fecha_ingreso']) != pd.to_datetime(fecha_ingreso) :
                            if verbose: print("Censo Abierto", dfCensoPaciente.iloc[0]['fecha_ingreso'], fecha_ingreso)
                            errores.append({'Fecha Ingreso' : fecha_ingreso, 'Fecha ingreso abierto': dfCensoPaciente.iloc[0]['fecha_ingreso'], 'Error' : 'Hay un censo activo y abierto con fecha de ingreso diferente'})

                        # 2.1.2 - Que la fecha del censo sea diferente. (Fecha secuencial)
                        if pd.to_datetime(fecha_censo) - pd.to_datetime(dfCensoPaciente.iloc[0]['fecha_censo']) == 0:
                            # 2.1.3 - Si es la misma fecha que la IPS sea diferente (referencia)
                            if dfCensoPaciente.iloc[0]['codigo_ips_id'] == dfY['Código habilitación IPS']:
                                if verbose: print("Censo mismo dia", dfCensoPaciente.iloc[0]['codigo_ips_id'], dfY['Código habilitación IPS'])
                                errores.append({'IPS Carga' : dfY['Código habilitación IPS'], 'IPS ingreso abierto': dfCensoPaciente.iloc[0]['codigo_ips_id'], 'Error' : 'Censo duplicado en al misma IPS'})
                        else:
                            dias_entre_censo = (pd.to_datetime(fecha_censo) - pd.to_datetime(dfCensoPaciente.iloc[0]['fecha_censo'])).days
                            if dias_entre_censo > 1:
                                if verbose: print("Dias Entre Censo:", dias_entre_censo, fecha_censo, dfCensoPaciente.iloc[0]['fecha_censo'])
                                errores.append({'Fecha Censo' : fecha_censo, 'Ultima fecha censo': dfCensoPaciente.iloc[0]['fecha_censo'], 'Error' : 'La secuencia de registros de censo abierto no se cumple'})
                                
                        # 2.1.4 - La fecha de cargue puede ser posterior (Cuantos días de distancia: Reglas de distancia)
                        
                        
                        dfY['reingreso'] = False
                    # 2.2 - Esta Cerrado - tiene fecha de egreso
                    else :
                        # 2.2.1 - Validar reingreso (El mismo diagnostico o solo el tiempo)
                        delta_ingreso = pd.to_datetime(fecha_censo) - pd.to_datetime(dfCensoPaciente.iloc[0]['fecha_censo'])
                        if verbose: print("Delta ingreso", delta_ingreso)
                        if delta_ingreso.days < dias_reingreso :
                            # TODO Preguntar si debe tener elmismo diagnóstico
                            dfY['reingreso'] = True
                        else:
                            dfY['reingreso'] = False
                # 3 - Cuandos se cierra automaticamente (egreso automatico)

                # Si es correcto agreguelo a los correctos
                if len(errores) == 0:
                    dfY['afiliado_id'] = afiliado.iloc[0]['id']
                    #  TODO: relacionar afiliacion
                    dfY['afiliacion_id'] = 18912
                    # dfY['afiliacion_id'] = afiliacion.iloc[0]['id']
                    if verbose: print(dfY)
                    dfValidos = dfValidos.append(dfY, ignore_index=True)
                else: 
                    dfNY = dfY.copy()
                    dfNY['Error'] = errores
                    dfNoCumple = dfNoCumple.append(dfNY, ignore_index=True)
        
        dfValidosSirius = dfValidos.copy()
        for i in range(dfTiposDeIngreso.shape[0]):
            desc = dfTiposDeIngreso.iloc[i]['description']
            idr = dfTiposDeIngreso.iloc[i]['id']
            dfValidosSirius['Tipo Ingreso'].replace(to_replace = desc, value = idr, inplace = True)
        for i in range(dfOrigenesEvento.shape[0]):
            desc = dfOrigenesEvento.iloc[i]['description']
            idr = dfOrigenesEvento.iloc[i]['id']
            dfValidosSirius['Origen Evento'].replace(to_replace = desc, value = idr, inplace = True)
        for i in range(dfTiposHabitacion.shape[0]):
            desc = dfTiposHabitacion.iloc[i]['description']
            idr = dfTiposHabitacion.iloc[i]['id']
            dfValidosSirius['Tipo Habitación'].replace(to_replace = desc, value = idr, inplace = True)
        for i in range(dfCondicionesAlta.shape[0]):
            desc = dfCondicionesAlta.iloc[i]['description']
            idr = dfCondicionesAlta.iloc[i]['id']
            dfValidosSirius['Condición de alta'].replace(to_replace = desc, value = idr, inplace = True)

        return dfValidos, dfNoCumple
        # validar segun las reglas, 

# NoCaracteresEspecialesValidationRule(nValues)
# TipoDeIdentificacionValidationRule(values, listaDocumentos=[])
# FechaNacimientoValidationRule(values)
# ValorEnListaValidationRule(values, listaRevision)
# NumeroTelefonicoValidationRule(values, maxPhoneNumbers=2, separator='-')
# FechaValidationRule(values, opcionesPorDefecto=[], umbralValido=5)
# CodigoCIEValidationRule(values, opcionesXDefecto=[])
# NumeroValidationRule(values, opcionesXDefecto=[])
# FechaExactaValidationRule(values, fecha)
# NumeroDocumentoValidationRule(values)
# CodigoMunicipioValidationRule(values, codigosMunicipios)
# ValorEnListaOpcionDefectoValidationRule(values, listaRevision, opcionDefecto)
# DummyValidationRule(values)
        

       

    