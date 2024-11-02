# views.py
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .serializers import BaseOwnerSerializer, OwnerSerializer, AgreementDocumentSerializer
from rest_framework.views import APIView
from user_management.models import Role
from django.contrib.auth import get_user_model
from .models import BaseOwner, AgreementDocument, AssetManagementOwner, BrokerageOwner
from .document import create_agreement_document 
from django.http import JsonResponse

User = get_user_model()

class BaseOwnerCreateView(generics.CreateAPIView):
    serializer_class = BaseOwnerSerializer

    def create(self, request, *args, **kwargs):
        try:
            print("Role of request user:", request.user.role.name)
            if request.user.role.name not in ['Admin', 'Superuser', 'Manager']:
                print('User does not have permission')
                return Response({"detail": "You do not have permission to create a user."}, status=status.HTTP_403_FORBIDDEN)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            
            owner = serializer.save()

            owner_details = {
                'name': owner.owner_name,
                'type': owner.owner_type,
                'agreement_type': owner.agreement_type,
                'contact': owner.user.phone_number if owner.user else None,
                'email': owner.user.email if owner.user else None,
            }

            agreement_details = {
                'contract_mode': request.data['contract_mode'],
                'revenue_type': request.data['revenue_type'],
                'contract_status': "Pending"
            }

            notes = "This is a note for the legal team regarding the agreement preparation."

            requestor_info = {
                'name': request.user.username,
                'role': request.user.role.name,
                'contact': request.user.phone_number if hasattr(request.user, 'phone_number') else 'N/A'
            }

            file_name, document_content = create_agreement_document(owner_details, agreement_details, notes, requestor_info)
            print(file_name, document_content)
            document = AgreementDocument.objects.create(
                owner=owner,
                document_type=owner.agreement_type,
                document_content=document_content,
            )

            response_data = {
                'owner': {
                    'id': owner.id,
                    'owner_name': owner.owner_name,
                    'owner_type': owner.owner_type,
                    'agreement_type': owner.agreement_type,
                    'email': owner.user.email,
                    'role': owner.user.role.name,
                }
            }

            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class MyOwnerView(APIView):
    def get(self, request, *args, **kwargs):
        owners = BaseOwner.objects.filter(user__role__name='Owner',is_verified_from_legal_team = True)
        serializer = OwnerSerializer(owners, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AgreementDocumentListView(generics.ListAPIView):
    queryset = AgreementDocument.objects.all()
    serializer_class = AgreementDocumentSerializer

class VerifyAgreementDocumentView(generics.UpdateAPIView):
    queryset = AgreementDocument.objects.all()
    serializer_class = AgreementDocumentSerializer

    def patch(self, request, *args, **kwargs):
        document_id = kwargs.get('id')
        try:
            document = self.get_object() 
            document.is_verified_from_legal_team = True
            document.save()
            return Response({'detail': 'Document verified successfully.'}, status=status.HTTP_200_OK)
        except AgreementDocument.DoesNotExist:
            return Response({'detail': 'Document not found.'}, status=status.HTTP_404_NOT_FOUND)

class UserAgreementDocumentsView(generics.ListAPIView):
    serializer_class = AgreementDocumentSerializer

    def get_queryset(self):
        user_id = self.kwargs.get('user_id')
        owner_id = BaseOwner.objects.get(user_id = user_id)
        return AgreementDocument.objects.filter(owner_id=owner_id.id,is_verified_from_legal_team=True)
    
class SignAgreementDocumentView(APIView):
    def post(self, request, id):
        try:
            document = AgreementDocument.objects.get(id=id)
            owner = BaseOwner.objects.get(id = document.owner_id)
            owner.is_verified_from_legal_team = True
            owner.save()
            document.status = "Signed"
            document.is_verified_from_legal_team = True
            document.save()

            return Response({"message": "Document status updated to Signed."}, status=status.HTTP_200_OK)

        except AgreementDocument.DoesNotExist:
            return Response({"error": "Document not found."}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)