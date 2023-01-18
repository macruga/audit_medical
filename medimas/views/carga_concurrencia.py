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
from medimas.models.carga_concurrencia import uploadFileConcurrenciaModel
# Import custom serializers
from medimas.serializers.carga_concurrencia import uploadFileConcurrenciaSerializer
# Permissions
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered   # Path to our custom permission


# Vista para la carga de archivos de concurrencia
class uploadFileConcurrenciaView(viewsets.ModelViewSet):
    # All views must contein a model  name for the permissions are efective, we get this from serializer, see:
    modulo = 'cargaConcurrencia'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    queryset = uploadFileConcurrenciaModel.objects.all()
    serializer_class = uploadFileConcurrenciaSerializer
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    # def update(self, request):
    #     raise serializers.ValidationError({'error':'No permitido!!'})

