import os, platform, logging
import core.settings as settings

"""
@Desc: El script se encarga de generar logs y almacenarlos de acuerdo al nombre de la aplicacion o modulo
que lo solicite
@param logname: string, nombre del archivo de logs
@output archivo de logs en la ruta establecida

"""

class Log:
    def __init__(self, logname, modulo):
        # Se define la ruta que  guardara los logs
        # print(settings.PATH_LOGS)
        self.modulo = modulo
        try:
            path_file = os.path.join(settings.PATH_LOGS, logname)
            print('Archivo Log en ', path_file)
            logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s : %(levelname)s : %(message)s',
                            filename = path_file,
                            filemode = 'w',)
        except Exception as error:
            print(error)       

        

    def start(self):        
        logging.debug('Inicia el modulo {}'.format(self.modulo))

    def info(self, mensaje):
        logging.info(mensaje)

    def error(self, mensaje):
        logging.error(mensaje)
    
    def warning(self, mensaje):
        logging.warning(mensaje)