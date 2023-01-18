from email import message
from genericpath import exists
from rest_framework import generics
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import serializers
from django.core import exceptions
import django.contrib.auth.password_validation as validators
# import for login
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate 
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from core.serializers.usuarios import UserSerializer, passwordUpdateSerializer
# Imports propios
from core.models.perfiles import PerfilModel
from core.permissions import IsActive, IsProfileAuth, IsModelRegistered 
from core.models.soporte.ips import IpsModel

User = get_user_model()

"""
@desc: modelo para la creacion de usuarios
@params: modulo string - nombre del modulo app el cual debe estar registrado en la modelo  modulos con el mismo nombre
@params: username string
@params: password string
@params: email string
@return: JSON con la informacion del usuario creado

"""

# Views for user creating
class passwordUpdate(viewsets.ModelViewSet):
    # All views must contein a model  name for the permissions are efective, we get this from serializer, see:
    modulo = 'Owner'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)


    def update(self, request):
        """
        Actualiza el password del usuario registrado
        """
        
        user = User.objects.get(id=self.request.user.id)
        serializer = passwordUpdateSerializer(data=request.data)  

        if serializer.is_valid():
            try:
                # validate the password and catch the exception
                validators.validate_password(password=request.data['password'], user=user)
                user.set_password(request.data['password'])
                user.save()
                return Response(status=status.HTTP_202_ACCEPTED)
                # the exception raised here is different than serializers.ValidationError
            except exceptions.ValidationError as e:
                print(list(e.messages))
                # return user
                raise serializers.ValidationError(e.messages) 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def list(self, instance): 
        return Response({"error": "Metodo no permitido"}, status=status.HTTP_403_FORBIDDEN)
   

    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        print(self)
        return '{}'.format( self.modulo )

# Model for users login, return token 
class LoginView(APIView):
    authentication_classes = ()
    permission_classes = ()
 
    def post(self, request,):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username=username, password=password)
        if user:
            # Token.objects.create(user=user)
            return Response({"token": user.auth_token.key})
        else:
            return Response({"error": "Credenciales incorrectas"}, status=status.HTTP_401_UNAUTHORIZED)

# Model for users logout, delete token
class LogoutView(APIView):
    permission_classes = ()
    def get(self, request, format=None):
        # simply delete the token to force a login
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)

# Model for view token user
class UserTokenView(APIView):
    # authentication_classes = ()
    # permission_classes = (AllowAny,)
    def post(self, request):
        token = request.data.get("token")
        userSearch = User.objects.filter(username=request.user).values()
        if (userSearch.count() > 0):
            for entry in userSearch: # converts ValuesQuerySet into Python list
                userData = entry
            # print(userData)
            validationToken = False
            if (token == userData['token']):
                validationToken = True
            return Response({"validation": validationToken}, status=status.HTTP_200_OK)
        else:
            return Response(status=status.HTTP_204_NO_CONTENT)

# Model for view info user
class UserJWTView(APIView):
    # authentication_classes = ()
    # permission_classes = (AllowAny,)
    def post(self, request):
        token = request.data.get("token")
        User.objects.filter( username=request.user ).update( token=token )
        userSearch = User.objects.filter(username=request.user).values()
        return Response(status=status.HTTP_200_OK)

# Vista para obtener la informacion del usuario que se encuentra registrado
class userView(APIView):
    # All views must contein a model  name for the permissions are efective, we get this from serializer, see:
    modulo = 'User'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    
    def get(self, request):
        grupos = User.objects.filter(id=request.user.id).values('group_profile') 
        ips_user = User.objects.filter(id=request.user.id).values('group_ips')       
        grupo_ips = []
        perfil = []   
        if ( grupos is not None ):
            for grupo in grupos:                
                reglas_accesos = PerfilModel.objects.filter( group_id = grupo['group_profile'], active = True).values('modulo__modulo', 'read', 'write', 'update').all()
                for regla in reglas_accesos:
                    perfil.append(regla)        
        for ips in ips_user:
            if ( ips['group_ips'] is not None ):
                ips_data = IpsModel.objects.filter(codigo_habilitacion = ips['group_ips']).values('codigo_habilitacion', 'ips', 'sucursal').all()
                grupo_ips.append(ips_data[0])
        response = {
            'username': request.user.username,
            'last_name': request.user.last_name,
            'first_name': request.user.first_name,
            'is_superuser': request.user.is_superuser,
            'group_profile': perfil,
            'group_ips': grupo_ips,

        }
        return Response( response, status=status.HTTP_200_OK)

    def __str__(self):
        return '{}'.format( self.modulo )



# Vista de consulta de usuarios
class UsersListView(viewsets.ModelViewSet):
    # All views must contain a model  name for the permissions are efective:
    modulo = 'User'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request):
        # Filtering consultas per user
        owner_id = request.user.id
        query = User.objects.all().order_by('-date_joined')
        serializer = UserSerializer(query, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        serializer = UserSerializer(data=request.data)
        # Assign owner from loggin user, if API fill it, get inmutable error, then pass
        try:
            request.data['owner'] = request.user.id          
        except:
            pass
        
        if serializer.is_valid():       
            serializer.save() 
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        query = User.objects.get(id=pk)
        serializer = UserSerializer(query)
        return Response(serializer.data)

    def update(self, request, pk=None):
        print(request.data)
        # Validations
        if request.data['username'] == '':
            return Response("El campo username es obligatorio", status=status.HTTP_400_BAD_REQUEST)
        if (User.objects.filter(username=request.data['username']).exclude(id = request.data['id']).exists()):
            return Response('El nombre de usuario ya existe!!', status=status.HTTP_409_CONFLICT)
        try:
            User.objects.filter( id = request.data['id'] ).update( 
                email=request.data['email'], is_superuser=request.data['is_superuser'], 
                is_active=request.data['is_active'], username=request.data['username'],
                cargo=request.data['cargo'], empresa=request.data['empresa'],
                first_name=request.data['first_name'], last_name=request.data['last_name'])
            # Get user to update profile
            user = User.objects.filter(id=pk)
            print(request.data['group_profile'])
            # user[0].group_profile.clear()
            print(request.data['group_profile'])
            for group in request.data['group_profile']:
                user[0].group_profile.add(group)
            return Response(status=status.HTTP_200_OK)
        except exceptions.ValidationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)



    # Vista de consulta de usuarios
class UserPassword(viewsets.ModelViewSet):
    # All views must contain a model  name for the permissions are efective:
    modulo = 'User'
    # Call classes for authorization model 
    permission_classes = (IsActive, IsProfileAuth, IsModelRegistered,)
    # permission_classes = ()
    # All views must contain def __str__ with model name for that the permission.py file can do  authorization filter
    def __str__(self):
        return '{}'.format( self.modulo )

    def list(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, pk=None):
        return Response(status=status.HTTP_401_UNAUTHORIZED)

    def update(self, request, pk=None):
        user = User.objects.get(id=pk)
        serializer = passwordUpdateSerializer(data=request.data)

        if serializer.is_valid(): 
            try:
                # validate the password and catch the exception
                validators.validate_password(password=request.data['password'], user=user)
                user.set_password(request.data['password'])
                user.save()
                return Response(status=status.HTTP_202_ACCEPTED)
            # the exception raised here is different than serializers.ValidationError
            except exceptions.ValidationError as e:
                print(list(e.messages))
                # return user
                raise serializers.ValidationError(e.messages)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        

    def destroy(self, request):
        return Response(status=status.HTTP_401_UNAUTHORIZED)