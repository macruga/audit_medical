from rest_framework import serializers
import django.contrib.auth.password_validation as validators
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from django.core import exceptions

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    # active = serializers.HiddenField(
    #     default=True,
    #     )
    
    def create(self, validated_data):
        """
        Creacion de usuarios
        """
        user = User(
            email = validated_data['email'],
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            phoneNumber = validated_data['phoneNumber'], 
            empresa = validated_data['empresa'], 
            cargo = validated_data['cargo'],
            group_profile = validated_data['group_profile'],
        )

        '''
        Borramos los arreglos de muchos a muchos suministrado en la data inicial, 
        en una directiva personalizada esta prohibido pasar datos de muchos a muchos directamente 
        Asi que primero se guardaran los datos de los grupos asignados y despues con .set(), 
        se agregan los datos de muchos a muchos al modelo '''

        # capturamos el arreglo de group_profile y group_ips, los guardamos y los borramos de la data principal
        if 'group_profile' in validated_data.keys(): # Si el campo es enviado en el payload
            groups_profile = validated_data['group_profile'] # Obtenemos group_profile en una arreglo
            del validated_data['group_profile']
        else: # Si el campo no se recibe se deja como un arreglo vacio
            groups_profile = []

        if 'group_ips' in validated_data.keys(): # Si el campo es enviado en el payload
            groups_ips = validated_data['group_ips'] # Obtenemos group_ips en una arreglo
            del validated_data['group_ips']
        else: # Si el campo no se recibe en el payload se deja como un arreglo vacio
            groups_ips = []

        try:
            # validate the password and catch the exception
            validators.validate_password(password=validated_data['password'], user=user)
            user.set_password(validated_data['password'])
            user.save()
            # Se asigna la pertinencia a grupos de perfil
            user.group_profile.set(groups_profile)
            # Se asigna la pertinencia a ips
            user.group_ips.set(groups_ips)
            return user
        # the exception raised here is different than serializers.ValidationError
        except exceptions.ValidationError as e:
            print(list(e.messages))
            # return user
            # TODO reemplazar por una respuesta http customizada
            raise serializers.ValidationError(e.messages)
    
    class Meta:
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name', 'phoneNumber', 'cargo', 'empresa', 'group_profile', 'group_ips', 'is_active', 'is_superuser', 'password']
        # fields = '__all__'
        extra_kwargs = {'password' : {'write_only' : True}}

class passwordUpdateSerializer(serializers.ModelSerializer):           
    class Meta:
        model = User
        fields = ['password']
        # fields = '__all__'
        extra_kwargs = {'password' : {'write_only' : True}}


class UserExpandSerializer(serializers.ModelSerializer):  

    class Meta:
        model = User
        fields = ('id','username', 'email', 'first_name', 'last_name')