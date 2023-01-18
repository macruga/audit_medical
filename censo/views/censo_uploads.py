from django.core.serializers import serialize
from rest_framework import serializers
from rest_framework import generics
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import filters
# Import custom models
from censo.models.censo_uploads import uploadFileCensoModel
# Import custom serializers
from censo.serializers.censo_uploads import uploadFileCensoSerializer
# Permissions
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered   # Path to our custom permission


# Censo upload file view
class uploadFileCensoView(viewsets.ModelViewSet):
    # TODO generar un archivo de variables de entorno  
    #  All views must contain a model  name for the permissions are efective:
    modulo = 'censoUpload'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    queryset = uploadFileCensoModel.objects.all()
    serializer_class = uploadFileCensoSerializer
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )


# Get uploads by user 
class uploadsUserView(viewsets.ModelViewSet):
    # All views must contein a model  name for the permissions are efective, we get this from serializer, see:
    modulo = 'uploadHistorical'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    queryset = uploadFileCensoModel.objects.all()
    serializer_class = uploadFileCensoSerializer
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def create(self, request):
        raise serializers.ValidationError('No permitido!!')

    def update(self, request):
        raise serializers.ValidationError('No permitido!!')

    def list(self, request):
        user = request.user.id
        if ( user == None ):
            raise serializers.ValidationError('Debe contener el parametro id user')                       
        queryset = uploadFileCensoModel.objects.filter(owner=int(user)).values('id','created','errors','errors_file',
        'errors_hash', 'errors_json','errors_json_hash','file','ips','ips__ips','success','success_file','success_hash','validated','validated',
        'errors_report', 'errors_report_hash').order_by('-created')
        return Response( queryset, status=status.HTTP_200_OK)

    