import pymssql
import pyodbc
import sqlalchemy as sqal
import urllib
from datetime import datetime

# ----- Parametros de conexion servicio SQL SMD ------ 
host = "smd-analitica.database.windows.net"
username = "smdadmin"
password = "SMD*2020**"
portdb = 1433
db = 'sirius'
# ------------------------------------------------------


"""
@desc: Clase para conecion a la base de datos (warehouse), se usa pyodbc y sqlalchemy como clientes de conexion
@param: server: string, servidor de base datos
@param: user: string, usuario de bases de datos
@param: password: string, password de la base de DataWareHouse
@param: default: boolean, True si la base de datos es un servidor MSSQL, False si es SQL Azure
@ouput: log: archivo de log donde se registrara los eventos de la clase
@output: engine: cliente conexion sqlalchemy

"""

class  MssqlAzure():
    # Constructor
    def __init__(self, hostname=host, user=username, pwd=password, port=portdb, database=db, default=False, echo=True):
        # Cliente para el manejo de consultas       
        # Motor con SQlalchemy para el envio de dataframes a al base de datos
        if ( default ):
            params = urllib.parse.quote_plus(r'Driver={ODBC Driver 17 for SQL Server};Server=tcp:' + hostname + ',' + str(port) + ';Database=' + database + ';Uid=' + user + ';Pwd=' + pwd + ';Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;')
        else:
            params = urllib.parse.quote_plus(r'Driver={ODBC Driver 17 for SQL Server};Server=tcp:' + hostname + ',' + str(port) + ';Database=' + database + ';Uid=' + user + ';Pwd=' + pwd + ';Connection Timeout=30;')
        conn_str = 'mssql+pyodbc:///?odbc_connect={}'.format(params)
        self.engine = sqal.create_engine(conn_str,echo=echo)
        # print('warehose connection stablished at {}'.format(datetime.today()))
        @sqal.event.listens_for(self.engine, "before_cursor_execute")
        def receive_before_cursor_execute(conn, cursor, statement, params, context, executemany):
            if executemany:
                cursor.fast_executemany = True
        conn = self.engine.raw_connection()