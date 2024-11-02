from rest_framework import generics, permissions
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from .models import CustomUser, Role
from .serializers import UserSerializer, LoginSerializer, CustomUserCreationSerializer, AgentSerializer
from django.http import JsonResponse
from django.views import View
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

class LoginView(generics.GenericAPIView):
    try:
        serializer_class = LoginSerializer
        permission_classes = [permissions.AllowAny]
        try:
            def post(self, request, *args, **kwargs):

                print("Request Data:", request.data)

                serializer = self.get_serializer(data=request.data)
                serializer.is_valid(raise_exception=True)
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)
                return Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    'user': {
                        'id': user.id,
                        'username': user.username,
                        'email': user.email,
                        'role': user.role.name if user.role else None,
                    }
                }, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
    except Exception as e:
        print(e)

# development purpose
class RegisterAdminView(View):
    def get(self, request, *args, **kwargs):
        if User.objects.filter(role__name='Admin').exists():
            return JsonResponse({'message': 'Admin user already exists.'}, status=400)
        
        legal_role, created = Role.objects.get_or_create(name='Legal Team')
        owner_role, created = Role.objects.get_or_create(name='Owner')
        manager_role, created = Role.objects.get_or_create(name='Manager')
        agent_role, created = Role.objects.get_or_create(name='Agent')
        admin_role, created = Role.objects.get_or_create(name='Admin')

        admin_user = User.objects.create_user(
            username='adminuser',
            email='admin@example.com',
            password='nasscript_crm',
            phone_number='1234567890',
            role=admin_role
        )
        admin_user.is_staff = True
        admin_user.is_superuser = True
        admin_user.save()

        return JsonResponse({'message': 'Admin user created successfully.'}, status=201)

class UserCreateView(generics.CreateAPIView):
    try:
        queryset = CustomUser.objects.all()
        serializer_class = CustomUserCreationSerializer
        permission_classes = [IsAuthenticated]

        def perform_create(self, serializer):
            try:
                user = serializer.save()
                return user
            except Exception as e:
                print("Error in perform_create:", e)
                raise 

        def create(self, request, *args, **kwargs):
            print("Role of request user:", request.user.role.name)
            if request.user.role.name not in ['Admin', 'Superuser']:
                print('User does not have permission')
                return Response({"detail": "You do not have permission to create a user."}, status=status.HTTP_403_FORBIDDEN)
            print(request.data)
            request.data['role'] = Role.objects.get(name=request.data['role']).id
            print(request.data)
            serializer = self.get_serializer(data=request.data)
            if not serializer.is_valid():
                print("Validation Errors:", serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            print("Validated Data:", serializer.validated_data)
            return super().create(request, *args, **kwargs)
    except Exception as e:
        print(e)

class MyAgentView(APIView):
    def get(self, request, *args, **kwargs):
        role = Role.objects.get(name = 'Agent').id
        agents = User.objects.filter(role = role)
        serializer = AgentSerializer(agents, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class MyLegalMemberView(APIView):
    def get(self, request, *args, **kwargs):
        role = Role.objects.get(name = 'Legal Team').id
        agents = User.objects.filter(role = role)
        serializer = AgentSerializer(agents, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)