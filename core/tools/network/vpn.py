"""
Clase para controlar el servico de conexiion de VPN del proveedor Fortinet
@Desc: El script se encarga de controlar, iniciar, detener o restablecer el tunel SSL cliente de fortinet
@param service: string, nombre del servicio, este debe estar creado y configurado el el servidor
!!!!!! Este servicio debe ser creado en la configuracion de cada cliente de forma autoamtica
@output booelan, true cuando la conexion esta establecia, false en caso contrario

"""

import os, platform, logging

# Constantes respuestas servicio no encontrador
NO_SERVICE_FOUND_MAC = 'sudo: service: command not found'

class  Forticlient():
    # Constructor
    def __init__(self, service):
        self.service = service

    def start(self):
        response = os.system('sudo service {} start'.format(self.service))
        print(self.service)
        print(response)
        # and then check the response...
        if response == 0:
            print('Client vpn success!')
            vpnstatus = True
        else:
            print('Client vpn error!')
            vpnstatus = False

        return vpnstatus
    
    def status(self):
        response = os.system('sudo service {} status | grep Active | tr -d " " | cut -d ":" -f 2 |cut -d "(" -f 1'.format(self.service))
        return response