import pymssql
from datetime import datetime


# --- Parametros de conexion servidor SQL Medimas ------ 
serverMDMAS = "10.109.12.240"
portMDMAS='64808'
userMDMAS = "USR_IMEDICAL"
passwordMDMAS = "9e7pwsPY*"
# ------------------------------------------------------


class  MssqlConn():
    def __init__(self, server, username, pwd, db, port_db=1433 ):
        print('Start client connection  at {}'.format(datetime.today()))
        print(port_db)
        self.client = pymssql.connect(host=server, user=username, port=port_db, password=pwd, server=db)
        print('Client connection stablished at {}'.format(datetime.today()))