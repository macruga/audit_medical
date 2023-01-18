
# Se debe declarar el dirctoio de la aplicacion si los scripts son llamados fuera del core

import sys
import os

# **** Importamos el core de django para usar los modelos de SIRIUS ****
import django
sys.path.append('/Users/manuel.cruz/Documents/github/SIRIUS_DATA')
os.environ['DJANGO_SETTINGS_MODULE'] = 'sirius.settings'
django.setup()
# **************************************************************************
                             
sys.path.insert(0, '/Users/manuel.cruz/Documents/github/SIRIUS_DATA') 
import pandas as pd

import core.settings as settings
from core.tools.databases.mssql_conect import MssqlConn
from core.tools.loggin import Log
from core.tools.network.ping import CheckPing
from core.tools.network.vpn import Forticlient
from rips.models.am_intermedia import AmIntermediaModel



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
TABLES = ['AMC1.vwAM_MEDICAMENTOS']

# !!!!!! ----- Parametros de conexion servicio SQL SMD ------ 
SERVER = "10.109.12.240"
USER = "USR_IMEDICAL"
PASS = "9e7pwsPY*"
DB = 'MDMAS_INFORMACION'
PORT = 64808
# ------------------------------------------------------

# Se inicia el log
log = Log('tabla_AM2', 'ingesta')
log.start()

# Log temporal para identificaciones
log_tmp = Log('pacientes', 'ingesta')
log_tmp.start()

class  PipeLine():
   # Constructor
   def __init__(self):
      # Se valida si existe conexion con la base de datos (VPN activa), para esto se usa el scrit de CheckPing en 'core/tools/network/ping'
      
      # Se crea instancia para validacion de la VPN para
      vpn_conection = Forticlient('vpn-medimas')
      # !!!!!!! para otros clientes traer la ip de la configuracion establecida en el proyecto
      self.ping = CheckPing('10.109.12.240')
      if (self.ping.start() == True):
          # Inico de conexion a la base de datos de analisis
         try:
            log.info('conectar a la base de datos')
            self.connMedimas = MssqlConn(SERVER, USER, PASS, DB, PORT )
         except Exception as e:
            # log de errores
            log.error(e)
            print('error: {}'.format(e))
                
         # ************************************************************************************************************
         # log.info('No se hay conexion a la base de datos')
         # # Se valida si la vpn se encuentra activata
         # if ( vpn_conection.status() == 'inactive'  ):
         #    log.info('La VPN se encuentra inactiva')
         #    # Si la vpn se encuentra inactiva se inicia el servicio
         #    log.info('inciando al conexion de la vpn')
         #    try:
         #       vpn_conection.start()
         #    except Exception as exp:
         #       log.error('Error intentando crear conexion con la vpn')
         #       log.error(exp)
         # else:
         #    # Se valida ping nuevamente
         #    if (self.ping.start() == False):
         #       log.error('Existe conexion con la VPN, pero no con la base de datos, informar al administrador')
         #       # !!! debe escribir el intento para ser reporcesado de acuedo al schedule
         
         # No existe conexion con la base de datos del cliente, se incia servicio de conexion de la vpn
         # ************************************************************************************************************
      else:
         log.error('No es posible conectarse a la base de datos')

   def ingestar(self, quey):
      # consultaMedicamentos = "SELECT * FROM {} WHERE numero_identificacion = '{}'".format(TABLES[0], paciente)       
      dataAM = pd.read_sql(query, self.connMedimas.client)
      log_tmp.info('Query consultados: ' + query)
      log_tmp.info('Registros encontrados: ' + str(len(dataAM)))
      return dataAM

   def saveData(self, data_frame, tipo):
      for i in range(len(data_frame)):         
         if tipo == 'AM':
            try:
               # print(data_frame.loc[i, "numero_factura"], data_frame.loc[i, "numero_unidades"])
               AmIntermediaModel.objects.create(
                  numero_factura = data_frame.loc[i, "numero_factura"], 
                  codigo_prestador = data_frame.loc[i, "codigo_prestador"],
                  tipo_identificacion_usuario = data_frame.loc[i, "tipo_Id_usuario"], 
                  numero_identifacion_usuario = data_frame.loc[i, "numero_identificacion"],
                  numero_autorizacion = data_frame.loc[i, "Numero_autorizacion"],
                  codigo_medicamento = data_frame.loc[i, "codigo_medicamento"],
                  codigo_tipo_medicamento = data_frame.loc[i, "tipo_medicamento"],
                  nombre_generico_medicamento = data_frame.loc[i, "nombre_generico_medicamento"],
                  forma_farmaceutica = data_frame.loc[i, "forma_farmaceutica"],
                  concentracion_medicamento = data_frame.loc[i, "Concentracion_medicamento"],
                  unidad_medida_medicamento = data_frame.loc[i, "unidad_medida_medicamento"],
                  numero_unidades = data_frame.loc[i, "numero_unidades"],
                  valor_unitario_medicamento = data_frame.loc[i, "Vlr_unitario_medicamento"],
                  valor_total_medicamento = data_frame.loc[i, "Vlr_total_medicamento"],
                  owner_id = 1
                  )
            except Exception as e:
               # log de errores
               log.error('error: {}'.format(e))
               pass



# Inicializa el pipeline
log.info('Inicializa el pipline')
instance = PipeLine()


total = len(settings.PACIENTES)
start = 0
end = 999
while start < total:
   query = "SELECT * FROM {} WHERE numero_identificacion in (".format(TABLES[0])
   while (start <= end):
      query += "'" + settings.PACIENTES[start] + "'"
      if (start != end):
         query += ","
      else:
         query += ")"
      start += 1
   # print(query)   
   end += 1000
   if (end > total - 1):
      end = total - 1
   log.info('Inicia ingesta de la informacion segmento bloque de datos: ' + str(start) + ' a ' + str(end))
   data = instance.ingestar(query)
   log.info('Se carga la data el tabla Am intermedia')
   instance.saveData(data,'AM')
log.info('Tarea terminada')
# print(query)
