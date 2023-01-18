
# Se debe declarar el dirctoio de la aplicacion si los scripts son llamados fuera del core

import sys
import os
import os.path as op

# **** Importamos el core de django para usar los modelos de SIRIUS ****
# import django
# sys.path.append('/var/www/html/sirius-core')
# os.environ['DJANGO_SETTINGS_MODULE'] = 'sirius.settings'
# django.setup()
# **************************************************************************
                             
sys.path.insert(0, '/Users/manuel.cruz/Documents/github/SIRIUS_DATA') 
import pandas as pd
import json

import core.settings as settings
from core.tools.databases.mssql_conect import MssqlConn
from core.tools.databases.mssql_azure import MssqlAzure
from core.tools.loggin import Log
from core.tools.network.ping import CheckPing
from core.tools.network.vpn import Forticlient




# from core.tools.databases.mssql import MSSQL


"""
Script de conexion contra la base de datos del cliente
@description:
1. Este escript dependiendo de la configuracion, intentara consumo a traves de base de datos directa (mssql o mysql), o de web services
   la carga mediante csv, se realiza usando otro script
2. Validara si se requiere conexion de vpn para realizar la conexion, de ser asi, controlara la conexion a dicha vpn
3. Este script esta definido para el cliente medimas, se omiten validaciones de configuracion y se realiza un pipeline de acuerdof
   a la configuracion ya conocida del cliente

@modelo conexion medimas:
1. Conexion tunel IPSEC cliente fortinet, script de conexion '/var/scripts/medimas/vpn/vpn-medimas.sh'
2. Conexion a base de datos MSSQL
3. Consulta de archivos RIPS mediante vistas ubicadas en la base de datos 'INFORMACION'

"""
#!!!!!!! Tablas hardcodeadas de RIPS, se deben traer los nombres de acuerdo a la configuracion del proyecto del cliente
TABLES = ['AMC1.vwAH_HOSPITALIZACION','AMC1.vwAC_CONSULTAS', 'AMC1.vwAU_URGENCIAS', 'AMC1.vwAP_PROCEDIMIENTOS', 'AMC1.vwAM_MEDICAMENTOS']

# Nombre del archivo a cargar
FILE = 'requeridosFull.csv'

# !!!!!! ----- Parametros de conexion servicio SQL SMD ------ 
SERVER = "10.109.12.240"
USER = "USR_IMEDICAL"
PASS = "9e7pwsPY*"
DB = 'MDMAS_INFORMACION'
PORT = 64808
# ------------------------------------------------------

# Se inicia el log
log = Log('ingesta', 'ingesta')
log.start()


# Carga del archivo a subir
# Cargamos los documentos  de todos los pacientes
dfPacientes = pd.read_csv(op.join(settings.DATA_DIR, FILE), sep=";")
print('Listado total de pacientes: {}'.format(dfPacientes.shape))
dfPacientes = dfPacientes.drop_duplicates()
print(dfPacientes)
LISTA_PACIENTES = dfPacientes['Documento'].astype(str)




class  PipeLine():
   # Constructor
   def __init__(self):
      # Se valida si existe conexion con la base de datos (VPN activa), para esto se usa el scrit de CheckPing en 'core/tools/network/ping'

      # Variable para almacenar los bloques con errores para reprocesarlos
      self.trace = {}
      self.trace['file'] = []
      self.trace['file'] = { 
         'name': FILE,
         'length': len(LISTA_PACIENTES),
         'errors': [], 
         'success': []
      }
      # Se crea instancia para validacion de la VPN para
      # vpn_conection = Forticlient('vpn-medimas')
      # !!!!!!! para otros clientes traer la ip de la configuracion establecida en el proyecto
      self.connSIRIUS = MssqlAzure()
      self.ping = CheckPing('10.109.12.240')
      if (self.ping.start() == True):
         # Inico de conexion a la base de datos de analisis
         self.connSIRIUS = MssqlAzure()
         try:
            log.info('conectar a la base de datos')
            self.connMedimas = MssqlConn(SERVER, USER, PASS, DB, PORT )            
         except Exception as e:
            # log de errores
            log.error(e)
            # print('error: {}'.format(e))
                
         
      else:
         log.error('No es posible conectarse a la base de datos')

   # Funcion para guardar la traza de los eventos 
   def saveTrace(self):
      with open('trace_am_2.json', 'w') as file:
         json.dump(self.trace, file, indent=5)


   def dataCleaning(self, data, tipo):
      data = data.drop_duplicates()
      data['numero_identificacion'] = data.apply(lambda x : str(x['numero_identificacion']).strip(), axis=1 )
      data['numero_factura'] = data.apply(lambda x : str(x['numero_factura']).strip(), axis=1 )  
      data['numero_autorizacion'] = data.apply(lambda x : str(x['numero_autorizacion']).strip(), axis=1 )
      data['codigo_prestador'] = data.apply(lambda x : str(x['codigo_prestador']).strip(), axis=1 )    
      if tipo == 'AH':
         data['hora_egreso'] = data.apply(lambda x : str(x['hora_egreso'])[:5], axis=1 )
      if tipo == 'AC':
         try:
            data['fecha_consulta'] = data['fecha_consulta'].apply(lambda x: x.strftime('%Y-%m-%d'))
         except:
            pass
      if tipo == 'AU':
         data['hora_salida_usuario_observacion'] = data.apply(lambda x : str(x['hora_salida_usuario_observacion'])[:5], axis=1 )
         try:
            data['fecha_ingreso_usuario_observacion'] = data['fecha_ingreso_usuario_observacion'].apply(lambda x: x.strftime('%Y-%m-%d'))
         except:
            pass
         try:
            data['fecha_ingreso_usuario_observacion'] = data['fecha_ingreso_usuario_observacion'].apply(lambda x: x.strftime('%Y-%m-%d'))
         except:
            pass
      if tipo == 'AP':
         # Si la fecha es datatime la pasa a string, en caso contrario la deja igual
         data['numero_identificacion'] = data.apply(lambda x : str(x['numero_identificacion']).strip(), axis=1 )
         data['numero_identificacion'] = data.apply(lambda x : str(x['numero_identificacion'])[:20], axis=1 )
         data['codigo_prestador'] = data.apply(lambda x : str(x['codigo_prestador']).strip(), axis=1 )
         data['codigo_prestador'] = data.apply(lambda x : str(x['codigo_prestador'])[:20], axis=1 )
         data['codigo_procedimiento'] = data.apply(lambda x : str(x['codigo_procedimiento']).strip(), axis=1 )
         data['codigo_procedimiento'] = data.apply(lambda x : str(x['codigo_procedimiento'])[:20], axis=1 )
         data['ambito_realizacion_procedimiento'] = data.apply(lambda x : str(x['ambito_realizacion_procedimiento']).strip(), axis=1 )
         data['ambito_realizacion_procedimiento'] = data.apply(lambda x : str(x['ambito_realizacion_procedimiento'])[:2], axis=1 )
         data['finalidad_procedimiento'] = data.apply(lambda x : str(x['finalidad_procedimiento']).strip(), axis=1 )
         data['finalidad_procedimiento'] = data.apply(lambda x : str(x['finalidad_procedimiento'])[:2], axis=1 )
         data['personal_atiende'] = data.apply(lambda x : str(x['personal_atiende']).strip(), axis=1 )
         data['personal_atiende'] = data.apply(lambda x : str(x['personal_atiende'])[:2], axis=1 )
         data['dx_principal'] = data.apply(lambda x : str(x['dx_principal']).strip(), axis=1 )
         data['dx_principal'] = data.apply(lambda x : str(x['dx_principal'])[:2], axis=1 )
         data['numero_autorizacion'] = data.apply(lambda x : str(x['numero_autorizacion'])[:20], axis=1 )
         data['dx_relacionado'] = data.apply(lambda x : str(x['dx_relacionado']).strip(), axis=1 )
         data['dx_relacionado'] = data.apply(lambda x : str(x['dx_relacionado'])[:2], axis=1 )
         data['dx_complicacion'] = data.apply(lambda x : str(x['dx_complicacion']).strip(), axis=1 )
         data['dx_complicacion'] = data.apply(lambda x : str(x['dx_complicacion'])[:2], axis=1 )
         data['forma_realizacion_acto_quirurgico'] = data.apply(lambda x : str(x['forma_realizacion_acto_quirurgico']).strip(), axis=1 )
         data['forma_realizacion_acto_quirurgico'] = data.apply(lambda x : str(x['forma_realizacion_acto_quirurgico'])[:4], axis=1 )    
         try:
            data['fecha_procedimiento'] = data['fecha_procedimiento'].apply(lambda x: x.strftime('%Y-%m-%d')) 
         except:
               pass 
      return data


   def ingestar(self, quey, tipo, start, end):
      # consultaMedicamentos = "SELECT * FROM {} WHERE numero_identificacion = '{}'".format(TABLES[0], paciente)  
      try:     
         data_ingested = pd.read_sql(query, self.connMedimas.client)
         # log_tmp.info('Query consultados: ' + query)
         clean_data = self.dataCleaning(data_ingested, tipo)
         log.info('Registros encontrados: ' + str(len(clean_data)))
         # for c in clean_data:
         #    if clean_data[c].dtype == 'object':
         #       print('Max length of column %s: %s\n' %  (c, clean_data[c].map(len).max()))
         self.trace['file']['success'].append({
            'star': start,
            'end': end,
            'origin': 'ingest'
         })
         self.saveTrace()
      except Exception as e:
         self.trace['file']['errors'].append({
            'star': start,
            'end': end,
            'origin': 'ingest',
            'error': str(e)
         })
         self.saveTrace()
         pass
      return clean_data



   # definicion de procesos
   def saveData(self, data_frame, tipo, start, end):
      if tipo == 'AH':
         try:
            data_frame.rename(columns={
               'tipo_Id_usuario': 'tipo_identificacion_usuario', 
               'numero_identificacion': 'numero_identifacion_usuario',
               'via_ingreso_institucion': 'codigo_via_ingreso_institucion',
               'fecha_ingreso': 'fecha_ingreso_usuario',
               'hora_Ingreso': 'hora_ingreso_usuario', 
               'causa_externa': 'codigo_causa_externa', 
               'Dx_principal_ingreso': 'dx_principal_ingreso',
               'Dx_principal_egreso': 'dx_principal_egreso',
               'Dx_relacionado_egreso_No_1': 'dx_relacionado1_egreso',
               'Dx_relacionado_egreso_No_2': 'dx_relacionado2_egreso', 
               'Dx_relacionado_egreso_No_3': 'dx_relacionado3_egreso', 
               'Dx_complicacion': 'dx_complicacion',
               'estado_salida': 'codigo_estado_salida',
               'Dx_causa_basica_muerte': 'dx_causa_muerte',
               'fecha_egreso': 'fecha_salida_usuario',
               'hora_egreso': 'hora_salida_usuario',
            },
            inplace=True)
            # Se borran columnas no necesarias
            data_frame = data_frame.drop(columns=['id','Origen','Fecha_Cargue'])
            # Agregamos el owner al data_frame            
            # data_frame = data_frame.assign(created = '2021-04-18')
            data_frame = data_frame.assign(owner_id = 1)
            data_frame = data_frame.assign(active = 1)
            pd.Timestamp.today()
            # print(data_frame)
            data_frame.to_sql(name='rips_ahintermediamodel', con=self.connSIRIUS.engine, if_exists='append', index=False)
            self.trace['file']['success'].append({
               'star': start,
               'end': end,
               'origin': 'save'
            })
            self.saveTrace()
         except Exception as e:
            # log de errores
            self.trace['file']['errors'].append({
               'star': start,
               'end': end,
               'origin': 'save',
               'error': str(e)
            })
            self.saveTrace()
            log.error('error: {}'.format(e))
            pass

      if tipo == 'AC':
         try:
            data_frame.rename(columns={
               'numero_identificacion': 'numero_identifacion_usuario',
               'tipo_Id_usuario': 'tipo_identificacion_usuario',
               'Fecha_consulta': 'fecha_consulta',
               'finalidad_consulta': 'codigo_finalidad_consulta', 
               'causa_externa': 'codigo_causa_externa',
               'codigo_dx_principal': 'codigo_diagnostico_principal',
               'codigo_dx_relacionado_no_1': 'codigo_diagnostico_relacionado1',
               'codigo_dx_relacionado_no_2': 'codigo_diagnostico_relacionado2', 
               'codigo_dx_relacionado_no_3': 'codigo_diagnostico_relacionado3', 
               'tipo_Dx_principal': 'codigo_tipo_diagnostico_principal',
               'vlr_Consulta': 'valor_consulta',
               'vlr_cuota_moderadora': 'valor_cuota_moderadora',
               'vlr_neto_pagar': 'valor_neto_pagar'
            },
            inplace=True)
            # Se borran columnas no necesarias
            data_frame = data_frame.drop(columns=['id', 'Fecha_consulta_date', 'Origen','Fecha_Cargue', 'Año_comp', 'Mes_comp', 'Dia_comp'])
            # Agregamos el owner al data_frame            
            # data_frame = data_frame.assign(created = '2021-04-18')
            data_frame = data_frame.assign(owner_id = 1)
            data_frame = data_frame.assign(active = 1)            
            data_frame.to_sql(name='rips_acintermediamodel', con=self.connSIRIUS.engine, if_exists='append', index=False)
            self.trace['file']['success'].append({
               'star': start,
               'end': end,
               'origin': 'save'
            })
            self.saveTrace()
         except Exception as e:
            # log de errores
            self.trace['file']['errors'].append({
               'star': start,
               'end': end,
               'origin': 'save',
               'error': str(e)
            })
            self.saveTrace()
            log.error('error: {}'.format(e))
            pass

      if tipo == 'AU':
         try:
            data_frame.rename(columns={
               'numero_identificacion': 'numero_identifacion_usuario',
               'tipo_id_usuario': 'tipo_identificacion_usuario', 
               'numero_identificacion': 'numero_identifacion_usuario',
               'fecha_ingreso_usuario_observacion': 'fecha_ingreso_usuario',
               'hora_ingreso_usuario_observacion': 'hora_ingreso_usuario', 
               'causa_externa': 'codigo_causa_externa',
               'dx_relacionado_salida_no_1': 'dx_relacionado1_salida',
               'dx_relacionado_salida_no_2': 'dx_relacionado2_salida', 
               'dx_relacionado_salida_no_3': 'dx_relacionado3_salida', 
               'destino_usuario_la_salida_observacion': 'codigo_destino_salida_usuario',
               'estado_salida': 'codigo_estado_salida',
               'causa_basica_muerte_urgencias': 'causa_basica_muerte',
               'fecha_salida_usuario_observacion': 'fecha_salida_usuario',
               'hora_salida_usuario_observacion': 'hora_salida_usuario'
            },
            inplace=True)
            # Se borran columnas no necesarias
            data_frame = data_frame.drop(columns=['id','Origen','Fecha_Cargue'])
            # Agregamos el owner al data_frame            
            # data_frame = data_frame.assign(created = '2021-04-18')
            data_frame = data_frame.assign(owner_id = 1)
            data_frame = data_frame.assign(active = 1)
            try:
               data_frame['fecha_ingreso_usuario'] = data_frame['fecha_ingreso_usuario'].apply(lambda x: x.strftime('%Y-%m-%d'))   
               data_frame['fecha_salida_usuario'] = data_frame['fecha_salida_usuario'].apply(lambda x: x.strftime('%Y-%m-%d'))  
            except:
               pass          
            data_frame.to_sql(name='rips_auintermediamodel', con=self.connSIRIUS.engine, if_exists='append', index=False)
            self.trace['file']['success'].append({
               'star': start,
               'end': end,
               'origin': 'save'
            })
            self.saveTrace()


         except Exception as e:
            # log de errores
            self.trace['file']['errors'].append({
               'star': start,
               'end': end,
               'origin': 'save',
               'error': str(e)
            })
            self.saveTrace()
            log.error('error: {}'.format(e))
            pass   

      if tipo == 'AP':
         try:
            data_frame.rename(columns={
               'numero_identificacion': 'numero_identifacion_usuario',
               'tipo_Id_usuario': 'tipo_identificacion_usuario', 
               'numero_identificacion': 'numero_identifacion_usuario',
               'ambito_realizacion_procedimiento': 'ambito_procedimiento',
               'personal_atiende': 'codigo_personal_atiende', 
               'dx_principal': 'codigo_diagnostico_principal',
               'dx_relacionado': 'diagnostico_relacionado',
               'dx_complicacion': 'complicacion', 
               'forma_realizacion_acto_quirurgico': 'forma_realizacion_acto_cx', 
               'vlr_procedimiento': 'valor_procedimiento'
            },
            inplace=True)
            # Se borran columnas no necesarias
            data_frame = data_frame.drop(columns=['id', 'fecha_procedimiento_date', 'Origen','Fecha_Cargue', 'Año_comp', 'Mes_comp', 'Dia_comp'])
            # Agregamos el owner al data_frame            
            # data_frame = data_frame.assign(created = '2021-04-18')
            data_frame = data_frame.assign(owner_id = 1)
            data_frame = data_frame.assign(active = 1)             
            # data_frame['fecha_salida_usuario'] = data_frame['fecha_salida_usuario'].apply(lambda x: x.strftime('%Y-%m-%d'))            
            data_frame.to_sql(name='rips_apintermediamodel_requeridos', con=self.connSIRIUS.engine, if_exists='append', index=False)
            self.trace['file']['success'].append({
               'star': start,
               'end': end,
               'origin': 'save'
            })
            self.saveTrace()

         except Exception as e:
            # log de errores
            self.trace['file']['errors'].append({
               'star': start,
               'end': end,
               'origin': 'save',
               'error': str(e)
            })
            self.saveTrace()
            log.error('error: {}'.format(e))
            pass   

      if tipo == 'AM':
         try:
            data_frame.rename(columns={
               'numero_identificacion': 'numero_identifacion_usuario',
               'tipo_Id_usuario': 'tipo_identificacion_usuario', 
               'numero_identificacion': 'numero_identifacion_usuario',
               'Numero_autorizacion': 'numero_autorizacion',
               'tipo_medicamento': 'codigo_tipo_medicamento',
               'Vlr_unitario_medicamento': 'valor_unitario_medicamento', 
               'Vlr_total_medicamento': 'valor_total_medicamento'
              
            },
            inplace=True)            
            # Se borran columnas no necesarias
            data_frame = data_frame.drop(columns=['id','Origen','Fecha_Cargue'])
            for column in data_frame():
               data_frame[column] = data_frame[column].apply(lambda x: str(x)) 
            # Agregamos el owner al data_frame            
            # data_frame = data_frame.assign(created = '2021-04-18')
            data_frame = data_frame.assign(owner_id = 1)
            data_frame = data_frame.assign(active = 1) 
            
            # data_frame['fecha_salida_usuario'] = data_frame['fecha_salida_usuario'].apply(lambda x: x.strftime('%Y-%m-%d'))            
            data_frame.to_sql(name='rips_amintermediamodel_requeridos', con=self.connSIRIUS.engine, if_exists='append', index=False)
            self.trace['file']['success'].append({
               'star': start,
               'end': end,
               'origin': 'save'
            })
            self.saveTrace()

         except Exception as e:
            # log de errores
            self.trace['file']['errors'].append({
               'star': start,
               'end': end,
               'origin': 'save',
               'error': str(e)
            })
            self.saveTrace()
            log.error('error: {}'.format(e))
            pass    

"""
 
 
"""

# Inicializa el pipeline
log.info('Inicializa el pipline')
instance = PipeLine()


total = len(LISTA_PACIENTES)
# total = 50321
start = 0
end = 300
flag = False
tipo = 'AM'
while start < total:
   log.info('Inicia ingesta de la informacion segmento bloque de datos: ' + str(start) + ' a ' + str(end))
   query = "SELECT * FROM {} WHERE numero_identificacion in {}".format(TABLES[4], tuple(LISTA_PACIENTES[start:end])) 
   
   data = instance.ingestar(query, tipo, start, end)
   # print(data)
   log.info('Se carga la data en tabla AP intermedia')
   instance.saveData(data, tipo, start, end)
   start = end + 1    
   end += 300
   if (end > total - 1): 
      end = total - 1          
   if (start >= end):
      break
log.info('Tarea terminada')
print(query)


# query = "SELECT * FROM {} WHERE numero_identificacion = '28982828'".format(TABLES[3]) 
# query = "SELECT * FROM {} WHERE numero_identificacion = '39161445'".format(TABLES[3])  
# query = "SELECT * FROM {} WHERE numero_identificacion = '25093537'".format(TABLES[3]) 
# query = "SELECT * FROM {} WHERE numero_identificacion = '41431089'".format(TABLES[3]) 
# data = instance.ingestar(query, tipo, start, end)
# print(data)
# log.info('Se carga la data en tabla AP intermedia')
# instance.saveData(data, tipo, start, end)