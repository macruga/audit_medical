"""
Clase para validar ping de una ip
@param ip: strin, direccion IP a consultar
@output booelan, true si el ping es exitoso, false en caso contrario

"""

import os

class  CheckPing():
    # Constructor
    def __init__(self, ip):
        # Cliente para el manejo de consultas
        self.hostname = ip

    def start(self):
        response = os.system("ping -c 1 " + self.hostname)
        # and then check the response...
        if response == 0:
            print('Client network success!')
            pingstatus = True
        else:
            print('Client network error!')
            pingstatus = False

        return pingstatus

    