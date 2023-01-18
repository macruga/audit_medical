

from censo.models.condicion_alta import condicionAltaCensoModel
from censo.models.origen_evento import OrigenEventoModel
from censo.models.tipo_habitacion import TipoHabitacionModel
from censo.models.tipo_ingreso import TipoIngresoModel
from core.models.soporte.cie10 import Cie10Model
from estancias.models.servicios_estancias import ServiciosEstanciaModel
from rest_framework import serializers
from datetime import datetime
from django.contrib.auth import get_user_model
import os.path as path
from django.conf import settings

import pandas as pd
from afiliados.models.afiliado import afiliadoModel
from censo.models.censo_uploads import uploadFileCensoModel
from core.models.soporte.ips import IpsModel
from censo.validators import fieldsValidation
from core.tools.databases.mssql_azure import MssqlAzure
from core.tools.storage.blob_storage import storageAzure
from core.tools.storage.files import delFolderContent
from core.tools.storage.hash import *
from estancias.models.estancia import EstanciaModel
from estancias.rules import *

User = get_user_model()

'''
A constant is created with the name of the container and the folder, 
For multi-tenant sirius, this constant must be defined by the name of the project or client

@desc  Upload  censo file, use post method to send the file, then save it to azure blob storage  
@param file: file, xlsx, txt, and csv only
@output It Save file to azure, validate the file structure and create a new register into uploadFileCensoModel
'''

# TODO -- Create config model
CONTAINER = 'ecoopsos'
FOLDER = 'censo'
TYPES = ['XLSX', 'XLS', 'CSV', 'TXT']
TMP_SUCCESS = 'media/tmp_files/success'
TMP_ERRORS = 'media/tmp_files/errors'

DX_PR = ['A153',	'A858',	'A86',	'A90',	'B207',	'B23',	'B238',	'B589',	'C101',	'C103',	'C159',	'C169',	
'C182',	'C229',	'C241',	'C25',	'C349',	'C412',	'C509',	'C574',	'C71',	'C712',	'C73',	'C762',	'C787',	'C819',	
'C859',	'C91',	'C910',	'D469',	'F058',	'G048',	'G35',	'G360',	'G468',	'G610',	'G629',	'G700',	'G710',	'G952',	
'H46',	'I460',	'I60',	'I601',	'I603',	'I609',	'I612',	'I619',	'I620',	'I629',	'I63',	'I633',	'I64',	'I651',	
'I652',	'I671',	'I679',	'I688',	'I710',	'I712',	'I713',	'I714',	'I716',	'I718',	'I719',	'I740',	'I743',	'J386',	
'J852',	'J869',	'J955',	'K712',	'K85',	'L100',	'M321',	'N170',	'N179',	'O141',	'O82',	'Q251',	'R001',	'R060',	
'R072',	'R074',	'R101',	'R103',	'R104',	'R25',	'R468',	'R509',	'R55',	'R568',	'R57',	'R570',	'R571',	'R578',	
'R579',	'S122',	'T810',	'T821',	'T823',	'T861',	'T868',	'T887',	'Z940',	'Z951',	'Z952',	'Z959',	'Z988']

DX_DIAS = [{'codigo': 'A418', 'dias': 5},	{'codigo': 'A419', 'dias': 5},	{'codigo': 'A858', 'dias': 3},	
{'codigo': 'A86', 'dias': 3},	{'codigo': 'A90', 'dias': 3},	{'codigo': 'B207', 'dias': 3},	
{'codigo': 'B23', 'dias': 3},	{'codigo': 'B238', 'dias': 3},	{'codigo': 'B342', 'dias': 5},	
{'codigo': 'B972', 'dias': 5},	{'codigo': 'C101', 'dias': 2},	{'codigo': 'C103', 'dias': 2},	
{'codigo': 'C159', 'dias': 2},	{'codigo': 'C169', 'dias': 2},	{'codigo': 'C182', 'dias': 2},	
{'codigo': 'C229', 'dias': 2},	{'codigo': 'C241', 'dias': 2},	{'codigo': 'C25', 'dias': 2},	
{'codigo': 'C349', 'dias': 2},	{'codigo': 'C412', 'dias': 2},	{'codigo': 'C509', 'dias': 2},	
{'codigo': 'C574', 'dias': 2},	{'codigo': 'C71', 'dias': 2},	{'codigo': 'C712', 'dias': 2},	
{'codigo': 'C73', 'dias': 2},	{'codigo': 'C762', 'dias': 2},	{'codigo': 'C787', 'dias': 2},	
{'codigo': 'C819', 'dias': 2},	{'codigo': 'C859', 'dias': 2},	{'codigo': 'C91', 'dias': 2},	
{'codigo': 'C910', 'dias': 2},	{'codigo': 'D32', 'dias': 3},	{'codigo': 'D352', 'dias': 3},	
{'codigo': 'D371', 'dias': 3},	{'codigo': 'D376', 'dias': 3},	{'codigo': 'D391', 'dias': 3},	
{'codigo': 'D430', 'dias': 3},	{'codigo': 'D432', 'dias': 3},	{'codigo': 'D445', 'dias': 3},	
{'codigo': 'D469', 'dias': 3},	{'codigo': 'D483', 'dias': 3},	{'codigo': 'D508', 'dias': 3},	
{'codigo': 'D648', 'dias': 3},	{'codigo': 'D649', 'dias': 3},	{'codigo': 'D739', 'dias': 2},	
{'codigo': 'E101', 'dias': 4},	{'codigo': 'E108', 'dias': 4},	{'codigo': 'E112', 'dias': 4},	
{'codigo': 'E131', 'dias': 4},	{'codigo': 'E878', 'dias': 3},	{'codigo': 'G404', 'dias': 3},	
{'codigo': 'G405', 'dias': 3},	{'codigo': 'G408', 'dias': 3},	{'codigo': 'G409', 'dias': 3},	
{'codigo': 'G410', 'dias': 3},	{'codigo': 'G459', 'dias': 3},	{'codigo': 'G500', 'dias': 3},	
{'codigo': 'I059', 'dias': 3},	{'codigo': 'I060', 'dias': 3},	{'codigo': 'I110', 'dias': 4},	
{'codigo': 'I120', 'dias': 3},	{'codigo': 'I200', 'dias': 5},	{'codigo': 'I209', 'dias': 5},	
{'codigo': 'I21', 'dias': 5},	{'codigo': 'I210', 'dias': 5},	{'codigo': 'I211', 'dias': 5},	
{'codigo': 'I212', 'dias': 5},	{'codigo': 'I219', 'dias': 5},	{'codigo': 'I24', 'dias': 5},	
{'codigo': 'I249', 'dias': 5},	{'codigo': 'I251', 'dias': 5},	{'codigo': 'I252', 'dias': 5},	
{'codigo': 'I255', 'dias': 5},	{'codigo': 'I26', 'dias': 3},	{'codigo': 'I260', 'dias': 3},	
{'codigo': 'I269', 'dias': 3},	{'codigo': 'I33', 'dias': 3},	{'codigo': 'I339', 'dias': 3},	
{'codigo': 'I350', 'dias': 3},	{'codigo': 'I352', 'dias': 3},	{'codigo': 'I358', 'dias': 3},	
{'codigo': 'I38', 'dias': 3},	{'codigo': 'I39', 'dias': 3},	{'codigo': 'I420', 'dias': 3},	
{'codigo': 'I441', 'dias': 3},	{'codigo': 'I442', 'dias': 3},	{'codigo': 'I447', 'dias': 3},	
{'codigo': 'I472', 'dias': 3},	{'codigo': 'I48', 'dias': 3},	{'codigo': 'I49', 'dias': 3},	
{'codigo': 'I499', 'dias': 3},	{'codigo': 'I500', 'dias': 4},	{'codigo': 'I509', 'dias': 4},	
{'codigo': 'I519', 'dias': 4},	{'codigo': 'I771', 'dias': 3},	{'codigo': 'I828', 'dias': 3},	
{'codigo': 'J12', 'dias': 5},	{'codigo': 'J128', 'dias': 5},	{'codigo': 'J129', 'dias': 5},	
{'codigo': 'J159', 'dias': 3},	{'codigo': 'J189', 'dias': 3},	{'codigo': 'J441', 'dias': 5},	
{'codigo': 'J449', 'dias': 5},	{'codigo': 'J80', 'dias': 5},	{'codigo': 'J81', 'dias': 5},	
{'codigo': 'J841', 'dias': 5},	{'codigo': 'J848', 'dias': 5},	{'codigo': 'J90', 'dias': 3},	
{'codigo': 'J960', 'dias': 5},	{'codigo': 'J961', 'dias': 5},	{'codigo': 'J969', 'dias': 5},	
{'codigo': 'J980', 'dias': 5},	{'codigo': 'J985', 'dias': 5},	{'codigo': 'K250', 'dias': 3},	
{'codigo': 'K359', 'dias': 3},	{'codigo': 'K563', 'dias': 3},	{'codigo': 'K65', 'dias': 5},	
{'codigo': 'K650', 'dias': 5},	{'codigo': 'K659', 'dias': 5},	{'codigo': 'K703', 'dias': 3},	
{'codigo': 'K746', 'dias': 3},	{'codigo': 'K800', 'dias': 3},	{'codigo': 'K805', 'dias': 3},	
{'codigo': 'K808', 'dias': 3},	{'codigo': 'K81', 'dias': 3},	{'codigo': 'K828', 'dias': 3},	
{'codigo': 'K830', 'dias': 3},	{'codigo': 'K833', 'dias': 5},	{'codigo': 'K922', 'dias': 3},	
{'codigo': 'N188', 'dias': 3},	{'codigo': 'N19', 'dias': 3},	{'codigo': 'N390', 'dias': 3},	
{'codigo': 'R001', 'dias': 3},	{'codigo': 'S065', 'dias': 3},	{'codigo': 'S066', 'dias': 3},	
{'codigo': 'S099', 'dias': 3},	{'codigo': 'S118', 'dias': 3},	{'codigo': 'S14', 'dias': 3},	
{'codigo': 'S272', 'dias': 3},	{'codigo': 'S317', 'dias': 3},	{'codigo': 'S318', 'dias': 3},	
{'codigo': 'S724', 'dias': 3},	{'codigo': 'U072', 'dias': 5},]

COHORTES_PR = ['CANCER', 'FIBROSIS QUISTICA', 'EPOC', 'DIALISIS']

# Upload file serializer
class uploadFileCensoSerializer(serializers.ModelSerializer):
     # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    active = serializers.HiddenField(
        default=True
        )
    validated = serializers.HiddenField(
        default=False
        )
    upload_name = serializers.HiddenField(
        default=''
        )
    def create(self, validated_data):
        # Get data
        username = str(self.context['request'].user.username)
        ips = str(validated_data['ips'])

        # Get file, type and name
        documentType = (validated_data['file'].name.split('.',-1))
        documentType = documentType[-1]
        documentType = documentType.upper()

        # Validate file type
        if (documentType not in TYPES):
            response = { 'Archivo':  'El archivo no tiene un formato valido para carga: {}'.format(str(validated_data['file'])),
                         'Formatos Validos': TYPES}
            raise serializers.ValidationError(response)

        # Validate IPS 
        validateIPS = User.objects.filter( group_ips = validated_data['ips'], id = self.context['request'].user.id ).last()
        if validateIPS is None:
            validIPS = User.objects.filter( id = self.context['request'].user.id ).values('group_ips')
            response = { 'Archivo':  'El usuario no tiene permisos para cargar censo en la IPS: {}'.format(str(validated_data['ips']))}
            raise serializers.ValidationError(response)
        # Rename file 
        validated_data['upload_name'] = validated_data['file'].name # Set original name 
        validated_data['file'].name = self.setFileName(username, ips, 'original', documentType)

        file_ = uploadFileCensoModel.objects.create(**validated_data)


        # Validate file structure
        # try:
        validate = fieldsValidation(str(file_.file), documentType)
        dfValidos, dfNoCumple = validate.validate(verbose=False)
        print('Total proccessed data', dfValidos.shape, dfNoCumple.shape)
        # dfValidos, dfNoCumple = validate.validate(verbose=True)
         # Create files to be downloaded
        if not dfNoCumple.empty:
            dfInvalidos2Correct = dfNoCumple[['Fecha Ingreso', 'Tipo Identificación', 'Núm. Identificación', 'Dx Ingreso', 'Tipo Ingreso', 'Origen Evento', 'Dx Actual', 'Tipo Habitación', 'Código habilitación IPS', 'Fecha Egreso', 'Condición de alta', 'Dx Egreso', 'Fecha Censo']]
            dfInvalidosErrors2Report = dfNoCumple[['Tipo Identificación','Núm. Identificación','Fecha Censo','Error']]
        else :
            dfInvalidos2Correct = pd.DataFrame()
            dfInvalidosErrors2Report = pd.DataFrame()

        # Send Valid to sirius
        if not dfValidos.empty:
            self._loadCensoToSirius(dfValidos)
            # Save files
            fileNameValids = self.setFileName(username, ips, 'success', documentType)
            dfValidos.to_excel(path.join(settings.BASE_DIR, TMP_SUCCESS, fileNameValids))
            hash_success = getHash(path.join(settings.BASE_DIR, TMP_SUCCESS, fileNameValids))

            successRegisters = 0
            for index, row in dfValidos.iterrows():

                # Search if afilaido es in estancias and estado is 1
                estancia = EstanciaModel.objects.filter(afiliado_id = row['afiliado_id'], estado = 1).exists()

                # Get instances
                afiliado_id = afiliadoModel.objects.get(id = row['afiliado_id'])
                dx_actual = Cie10Model.objects.get(codigo = row['Dx Actual'])
                tipo_habitacion = TipoHabitacionModel.objects.get(description = row['Tipo Habitación'])
                tipo_ingreso = TipoIngresoModel.objects.get(description = row['Tipo Ingreso'])
                origen_evento = OrigenEventoModel.objects.get(description = row['Origen Evento'])
                ips = IpsModel.objects.get(codigo_habilitacion = row['Código habilitación IPS'])
                successTransaction = False

                # If afiliado is in estancias and estado is 1, then update estancia
                if estancia:
                    # Get estancia instance
                    estancia = EstanciaModel.objects.filter(afiliado_id = row['afiliado_id'], estado = 1).last()
                    # If fecha_fin is null, then update dx_actual in estancia and Tipo Habitacion
                    if pd.isnull(row['Fecha Egreso']):
                        # Update estancia
                        estancia.dx_actual = dx_actual
                        estancia.save()
                        successTransaction = True
                        successRegisters += 1
                        
                        
                    # If fecha_fin is not null, then update fecha_egreso, condicion_alta, dx_egreso in estancia
                    else:
                        # Get instances
                        condicion_alta = condicionAltaCensoModel.objects.get(description = row['Condición de alta'])
                        dx_egreso = Cie10Model.objects.get(codigo = row['Dx Egreso'])

                        # rules
                        _rule1 = EgresoMayorAIngresoRule( 
                            fecha_ingreso=row['Fecha Ingreso'], fecha_egreso=row['Fecha Egreso'] ).validate()
                        if _rule1[0]:
                                dfInvalidos2Correct = dfInvalidos2Correct.append(row)
                                dfInvalidosErrors2Report = dfInvalidosErrors2Report.append(
                                    {'Tipo Identificación': row['Tipo Identificación'], 
                                    'Núm. Identificación': row['Núm. Identificación'], 
                                    'Fecha Censo': row['Fecha Censo'], 
                                    'Error': _rule1[1]}, ignore_index=True)
                        else:
                            # Update estancia
                            estancia.fecha_egreso = row['Fecha Egreso']
                            estancia.condicion_alta_id = condicion_alta
                            estancia.dx_egreso = dx_egreso
                            estancia.estado = 0
                            estancia.usuario_egreso = self.context['request'].user
                            estancia.fecha_registro_egreso = datetime.now()
                            estancia.save()
                            successTransaction = True
                            successRegisters += 1

                        
                       
                # If afiliado is not in estancias, then create estancia
                else:
                    # Rules
                    _rule2 = RangoEstanciaRule(
                        afiliado_id=row['afiliado_id'], fecha_ingreso=row['Fecha Ingreso']).validate()
                    if _rule2[0]:
                        dfInvalidos2Correct = dfInvalidos2Correct.append(row)
                        dfInvalidosErrors2Report = dfInvalidosErrors2Report.append(
                            {'Tipo Identificación': row['Tipo Identificación'], 
                            'Núm. Identificación': row['Núm. Identificación'], 
                            'Fecha Censo': row['Fecha Censo'], 
                            'Error': _rule2[1]}, ignore_index=True)
                    else:
                        estancia = EstanciaModel()
                        estancia.afiliado_id = afiliado_id
                        estancia.fecha_ingreso = row['Fecha Ingreso']
                        estancia.dx_ingreso = dx_actual
                        estancia.dx_actual = dx_actual
                        estancia.tipo_ingreso_id = tipo_ingreso
                        estancia.origen_evento_id = origen_evento
                        estancia.codigo_ips_id = ips
                        estancia.estado = 1
                        estancia.owner = self.context['request'].user
                        estancia.save()
                        successTransaction = True
                        successRegisters += 1

                if successTransaction:
                    # save servicio estancia
                    ServiciosEstanciaModel.objects.create(
                        estancia_id = estancia,
                        tipo_habitacion_id = tipo_habitacion,
                        fecha = row['Fecha Ingreso'],
                        owner_id = self.context['request'].user.id
                    )
        else:
            fileNameValids = ""
            hash_success = ""

        # Get name to records with errors
        if dfInvalidos2Correct.shape[0] > 0:
            fileNameErrors = self.setFileName(username, ips, 'errors', documentType)
            dfInvalidos2Correct.to_excel(path.join(settings.BASE_DIR, TMP_ERRORS, fileNameErrors))
            hash_errors = getHash(path.join(settings.BASE_DIR,TMP_ERRORS, fileNameErrors))
            # Formato de reporte de errores para la corrección
            fileNameErrorsRep = self.setFileName(username, ips, 'errors_report', documentType)
            dfInvalidosErrors2Report.to_excel(path.join(settings.BASE_DIR, TMP_ERRORS, fileNameErrorsRep))
            hash_report = getHash(path.join(settings.BASE_DIR, TMP_ERRORS, fileNameErrorsRep))
            # Save trace records in json format
            fileNameErrorsRepJson = self.setFileName(username, ips, 'errors', 'json')
            dfInvalidosErrors2Report.to_json(path.join(settings.BASE_DIR, TMP_ERRORS, fileNameErrorsRepJson))
            hash_report_json = getHash(path.join(settings.BASE_DIR, TMP_ERRORS, fileNameErrorsRepJson))
        else:
            dfInvalidos2Correct = ""
            hash_errors = ""
            dfInvalidosErrors2Report = ""
            hash_report = ""
            dfInvalidosErrors2Report = ""
            hash_report_json = ""
            fileNameErrors = ""
            fileNameErrorsRepJson = ""
            fileNameErrorsRep = ""


        

        # Change validation status file
        uploadFileCensoModel.objects.filter( id = file_.id ).update( 
            validated = True , success=successRegisters, success_file=fileNameValids, 
            success_hash = hash_success, errors=dfInvalidos2Correct.shape[0], 
            errors_file=fileNameErrors, errors_hash=hash_errors, 
            errors_json=fileNameErrorsRepJson, errors_json_hash=hash_report_json,
            errors_report=fileNameErrorsRep, errors_report_hash=hash_report
        )
        # validated_data['validated'] = True
        # validated_data['success'] = dfValidos.shape[0]
        # validated_data['success_file'] = fileNameValids
        # validated_data['success_hash'] = getHash(path.join(settings.BASE_DIR, TMP_SUCCESS, fileNameValids))
        # validated_data['errors'] = dfNoCumple.shape[0]
        # validated_data['errors_file'] = fileNameErrors
        # validated_data['errors_hash'] = getHash(path.join(settings.BASE_DIR,TMP_ERRORS, fileNameErrors))
        # validated_data['errors_json'] = fileNameErrorsRep
        # validated_data['errors_json_hash'] = getHash(path.join(settings.BASE_DIR, TMP_ERRORS, fileNameErrorsRep))

        
        
        for error in dfNoCumple['Error'].to_list():
            print(str(error))
        # # except KeyError as ke:
        # except Exception as err:
        #     # TODO 
        #     print(err)

        file__ = uploadFileCensoModel.objects.filter(id=int(str(file_)))
        for file_final in file__:
            print(file_final)
        return file_final

  
    def to_representation(self, instance): 
        '''
        Send IPS name in data representation
        
        '''     
        # Use this for raiser error
        # raise serializers.ValidationError(error)
        data = super().to_representation(instance) 
        data['ips__name'] = str(instance.ips.ips)
        return data



    def _loadCensoToSirius(self, dfValidRecords):
        '''_loadCensoToSirius(self, dfValidRecords)
        Send the valid records to the SIRIUS Data Ware House

        PARAMETERS
        ----------
        dfValidRecords: pandas.DataFrame
            Dataframe with the valid records of the uploaded censo
        '''
        # Rename columns to send valid records to SIRIUS
        dfValidRecords = dfValidRecords.rename(columns={
            'Tipo Identificación' : 'tipo_identificacion_id', 
            'Núm. Identificación' : 'identificacion',
            'Fecha Ingreso' : 'fecha_ingreso', 
            'Dx Ingreso' : 'dx_ingreso', 
            'Tipo Ingreso' : 'tipo_ingreso_id', 
            'Origen Evento' : 'origen_evento_id', 
            'Fecha Censo' : 'fecha_censo', 
            'Dx Actual' : 'dx_actual',
            'Tipo Habitación' : 'tipo_habitacion_id', 
            'Código habilitación IPS' : 'codigo_ips_id', 
            'Fecha Egreso' : 'fecha_egreso', 
            'Condición de alta' : 'condicion_alta_id', 
            'Dx Egreso' : 'dx_egreso', 
            #'created', 'active', 'owner_id',
        })
        # Add additional information to records
        created = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # created = pd.to_datetime('now')
        active = True
        owner_id = self.context['request'].user.id
        dfValidRecords['created'] = created
        dfValidRecords['active'] = active
        dfValidRecords['owner_id'] = owner_id
         
        # Establish a connection to the database instance
        bdConn = MssqlAzure(echo=False)
        # bdConn = MssqlAzure()
        # Map the reference values
        dfValidRecords = self.__mapReferenceValues(dfValidRecords, bdConn)
        # Ensure datatypes
        # dfValidRecords['']
        # dfValidRecords['condicion_alta_id'] = dfValidRecords['condicion_alta_id'].astype(int)
        dfValidRecords['identificacion'] = dfValidRecords['identificacion'].astype(str)
        dfValidRecords['dias_estancia'] = dfValidRecords['dias_estancia'].astype(int)
        dfValidRecords['reingreso'] = dfValidRecords['reingreso'].astype(int)
        dfValidRecords['afiliado_id'] = dfValidRecords['afiliado_id'].astype(int)
        # !!!!!dfValidRecords['afiliacion_id'] = dfValidRecords['afiliacion_id'].astype(int)
        del dfValidRecords['afiliacion_id']

        # send to sirius
        # print(dfValidRecords.dtypes)
        # print(dfValidRecords)
        dfValidRecords.to_sql('censo_censomodel', bdConn.engine, index=False, if_exists="append", chunksize=50)
        print("Cargado")
        

    def __mapReferenceValues(self, dfValidRecords, dbConnection):
        ''' mapReferenceValues(dfValidRecords, dbConnection)
        Mapea los valoresde las listas a las correspondientes llaves de las tablas de referencia

        PARAMETERS
        ----------
        dfValidRecords: pandas.DataFrame
            Data frame copn lso valores del censo valido
        dbConnection: MsSQLAzure.Connection
            Objeto para al conexión y transacciones con la base de datos 

        RETURNS
        -------
        pandas.DataFrame 
            DataFrame with the mapped values
        '''
        # print(dfValidRecords)
        data = pd.read_sql("select * FROM censo_tipoingresomodel", dbConnection.engine)
        data = data[data['active']==True][['id', 'description']]
        dfValidRecords['tipo_ingreso_id'] = dfValidRecords['tipo_ingreso_id'].map(data.set_index('description')['id'])
        data = pd.read_sql("select * FROM censo_origeneventomodel", dbConnection.engine)
        data = data[data['active']==True][['id', 'description']]
        dfValidRecords['origen_evento_id'] = dfValidRecords['origen_evento_id'].map(data.set_index('description')['id'])
        data = pd.read_sql("select * FROM censo_tipohabitacionmodel", dbConnection.engine)
        data = data[data['active']==True][['id', 'description']]
        dfValidRecords['tipo_habitacion_id'] = dfValidRecords['tipo_habitacion_id'].map(data.set_index('description')['id'])
        # print(dfValidRecords[['tipo_ingreso_id','origen_evento_id', 'tipo_habitacion_id', 'condicion_alta_id','tipo_identificacion_id', 'identificacion']], data, type(data))
        data = pd.read_sql("select * FROM censo_condicionaltacensomodel", dbConnection.engine)
        data = data[data['active']==True][['id', 'description']]
        dfValidRecords['condicion_alta_id'] = dfValidRecords['condicion_alta_id'].map(data.set_index('description')['id'])

        return dfValidRecords



    def setFileName(self, string1, string2, type_file, ext):
        '''
        Create variable with custom file name: "date_string1_string2_type.ext"

        PARAMETERS
        ----------
        string1: string
            First string of the format 
        string2: string
            First string of the format
        type_file: string
            File type
        ext: string
            File extension
        '''
        name = '{}_{}_{}_{}.{}'.format(datetime.now().strftime('%Y-%m-%d %H%M%S') ,string1, string2, type_file, ext.lower())
        return name


    class Meta:
        model= uploadFileCensoModel
        fields = '__all__'