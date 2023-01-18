'''
Script para realizar la carga de datos iniciales de la app
el script cargara archivos CSV con los datos de los modelos que deben ser inicializados
se deben parametrizar el areglo de modelos y el de files para que el algoritmo realice 
la carga de datos incial en cada uno de los modelos
'''
import os
import sys
import pandas as pd
import django

# Importar modelos
# TODO variable en settings
PATH = '/Users/manuel.cruz/Documents/github/backend_clico'
sys.path.append(PATH)
os.environ['DJANGO_SETTINGS_MODULE'] = 'sirius.settings'
django.setup()

from core.models.soporte.cohorte import CohorteModel
from core.models.soporte.aseguradoras import aseguradorasModel
from core.models.soporte.regimen import RegimenModel




def main():

    # Setup
    FILES_PATH = f"{PATH}/data_csv/"
    MODELS = [CohorteModel, RegimenModel, aseguradorasModel ]
    FILES = ['cohortes']#, 'regimenes', 'aseguradoras']

    data_to_load = zip(MODELS,FILES) # Cada modelo debe tener su archivo correspondiente de carga

    for data in data_to_load:
        model = data[0]
        _file = pd.read_csv(f'{FILES_PATH}{data[1]}.csv')
        _bulk = data[0](**_file.to_dict())
        model.objects.bulk_create([
            model(**dict(row))
            for index, row in _file.iterrows()])


if __name__ == '__main__':
    main()

