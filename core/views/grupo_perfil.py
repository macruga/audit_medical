from rest_framework import viewsets

# Imports propios
from core.models.grupo_perfil import GrupoPerfil
from core.serializers.grupo_perfil import GroupPerfilSerializer
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 

class GroupPerfilView(viewsets.ModelViewSet):
    # All views must contein a model  name for the permissions are efective, we get this from serializer, see:
    modulo = 'GroupPerfil'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth,)
    queryset = GrupoPerfil.objects.all()
    serializer_class = GroupPerfilSerializer
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )