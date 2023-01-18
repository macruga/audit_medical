from rest_framework import serializers
from medimas.models.carga_concurrencia import uploadFileConcurrenciaModel
from core.tools.storage.blob_storage import storageAzure
from core.tools.storage.files import delFolderContent

# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# Se crea una constante con el nombre del contenedor y el folder, esto para el cliente medimas, 
# para otros se debe traer de la configuracion del proyecto del cliente
CONTAINER_MDMAS = 'concurrencia-medimas'
FOLDER_CONCURRENCIA = 'concurrencia'

# Upload file serializer
class uploadFileConcurrenciaSerializer(serializers.ModelSerializer):
     # Save owner
    owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
        )
    active = serializers.HiddenField(
        default=True
        )
    procesado = serializers.HiddenField(
        default=False
        )
    def create(self, validated_data):
        # Get file and name
        # filename = self.context['request'].data.get("file")        
        # file = self.context['request'].FILES["file"]
        fileName = str(validated_data['file']).replace(' ', '_')
        
        print(fileName)
        # Quitar comentarios si se quiere validar que el nombre del archivo sea unico
        # uploads =  uploadFileConcurrenciaModel.objects.filter(file=fileName).last()
        # print(uploads)
        # if (uploads is not None):
        #     response = { 'Archivo':  'Ya existe un archivo relacionado al caso con el nombre: {}'.format(str(validated_data['file']))}
        #     raise serializers.ValidationError(response)
        
        file_ = uploadFileConcurrenciaModel.objects.create(**validated_data)
        print(file_.file)
        storage = storageAzure(validated_data['file'],str(file_.file),CONTAINER_MDMAS,FOLDER_CONCURRENCIA)
        storage.uploadFile()
        # Se limpia el directorio local de uploads 
        delFolderContent()
        
    class Meta:
        model= uploadFileConcurrenciaModel
        fields = '__all__'