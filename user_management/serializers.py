from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Role
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    role = serializers.CharField(write_only=True) 
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'phone_number', 'role', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        role_name = validated_data.pop('role')
        role = Role.objects.get(name=role_name) 
        validated_data['role'] = role
        user = CustomUser.objects.create(**validated_data)
        return user
    
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    try:
        def validate(self, attrs):
            try:
                print('try catch')
                email = attrs.get('email')
                password = attrs.get('password')

                if email and password:
                    user = authenticate(email=email, password=password)
                    print(email, password)
                    print(user)
                    if not user:
                        raise serializers.ValidationError('Invalid credentials')
                else:
                    raise serializers.ValidationError('Must include "email" and "password".')

                attrs['user'] = user
                return attrs
            except Exception as e:
                print(e)
    except Exception as e:
        print('validate error',e)

class CustomUserCreationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'username', 'email', 'phone_number', 'password', 'role', 'description']
        extra_kwargs = {
            'password': {'write_only': True},  
        }
    print('asldkjflaksjdf')
    try:
        print('try')
        def create(self, validated_data):
            try:
                print(validated_data)
                role_name = validated_data.pop('role')
                role = Role.objects.get(name=role_name)
            except ObjectDoesNotExist:
                raise serializers.ValidationError({"role": "Role does not exist."})

            user = CustomUser(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                username=validated_data['username'],
                email=validated_data['email'],
                phone_number=validated_data['phone_number'],
                role=role,
                description=validated_data['description']
            )
            
            user.set_password(validated_data['password'])
            user.save()
            return user
    except Exception as e:
        print(e)

class AgentSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'