"""
@prere: pip install azure-storage-blob 
@Desc: Scrip para realizar el envio de una archivo cargado al blobstorage de azure
@param: file: file, Archivo que se enviara al blobstorage
@param: filename: string, nombre del archivo que sera enviado al blob
@param: folder: string, nombre del folder del contenedor de los archivos en el blob 

"""

import os, uuid
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import datetime

# from rest_framework import serializers

class storageAzure():
        
    # local_path = "/Users/manuel.cruz/Documents/github/backendMedimas/api/storage/"
    # local_file_name = "a.txt"
    # upload_file_path = os.path.join(local_path, local_file_name)

    # init method or constructor
    def __init__(self, fileName, container, folder):
        self.fileName = fileName
        self.now = datetime.datetime.now()

        connect_str = 'DefaultEndpointsProtocol=https;AccountName=analitica6331787841;AccountKey=nRCTFO8H0As/WSVNOFQNoSjUGv7jBYTRq50MZRM7tlkI/3WlMTxAJhABZ3iOn3AWLLDhF5dN2B6nf1BzArAzJA==;EndpointSuffix=core.windows.net'
        
        # Cliente para conexion con azure storage
        blob_service_client = BlobServiceClient.from_connection_string(connect_str)
        
        # Instantiate a new ContainerClient
        container_name = container + '/' + folder + '/' + self.now.strftime('%Y-%m-%d')
        container_client = blob_service_client.get_container_client(container_name)
        
        if container_client.exists == False:
            # Create new Container in the service
            container_client.create_container()
        
        # Instantiate a new BlobClient
        self.blob_client = container_client.get_blob_client(fileName)       
        
        return
    # Upload file
    def uploadFile(self, path):  
        # Upload file    
        with open(path, "rb") as data:
            self.blob_client.upload_blob(data, blob_type="BlockBlob")  
        

    # Get file list
    def getFile(self):
        blob_list = self.container_client.list_blobs()

    