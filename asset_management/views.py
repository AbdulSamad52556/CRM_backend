from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import viewsets
from .models import Property, Unit
from .serializers import PropertySerializer, UnitSerializer
from user_management.models import CustomUser
from crm.models import BaseOwner
from rest_framework import generics
from rest_framework.permissions import AllowAny

class PropertyCreateView(APIView):
    def post(self, request):
        print(request.data)
        try:
            serializer = PropertySerializer(data=request.data, context={'request': request})
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PropertyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer

    def get_queryset(self):
        query_set = super().get_queryset()
        user_id = self.request.query_params.get('userId')
        
        if user_id:
            user = BaseOwner.objects.get(user = user_id)
            query_set = query_set.filter(owner=user)

        return query_set

class UnitCreateView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = UnitSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UnitListView(generics.ListAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

class PropertyListView(generics.ListAPIView):
    queryset = Property.objects.all()
    serializer_class = PropertySerializer  
    permission_classes = [AllowAny]  # Ensure this allows access
