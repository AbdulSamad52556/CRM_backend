from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import BaseOwner, BrokerageOwner, AssetManagementOwner, AgreementDocument
from user_management.models import Role

User = get_user_model()  

class BrokerageOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = BrokerageOwner
        fields = ['contract_mode']

class AssetManagementOwnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetManagementOwner
        fields = ['contract_mode', 'revenue_type']

class BaseOwnerSerializer(serializers.ModelSerializer):

    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(write_only=True, min_length=8)
    role = serializers.CharField(write_only=True) 
    phone_number = serializers.CharField(write_only=True)

    agreement_type = serializers.CharField()
    contract_mode = serializers.CharField()
    revenue_type = serializers.CharField(required=False, allow_blank=True, allow_null=True)

    class Meta:
        model = BaseOwner
        fields = ['owner_name', 'owner_type', 'role', 'phone_number', 'email', 'password', 'agreement_type', 'contract_mode', 'revenue_type']

    def create(self, validated_data):
        print(validated_data)
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        role_name = validated_data.pop('role')
        phone_number = validated_data.pop('phone_number')

        agreement_type = validated_data.pop('agreement_type')
        contract_mode = validated_data.pop('contract_mode')
        revenue_type = validated_data.pop('revenue_type', None)

        try:
            role = Role.objects.get(name=role_name)
        except Role.DoesNotExist:
            raise serializers.ValidationError({"role": "Role not found."})
        print(role)

        user = User.objects.create(username=email, email=email, role=role, phone_number = phone_number)
        print(user)
        user.set_password(password)
        user.save()

        owner = BaseOwner.objects.create(user=user, **validated_data, agreement_type=agreement_type)
        if agreement_type == 'Brokerage':
            BrokerageOwner.objects.create(owner=owner, contract_mode=contract_mode)
        elif agreement_type == 'Asset Management':
            AssetManagementOwner.objects.create(owner=owner, contract_mode=contract_mode, revenue_type=revenue_type)

        print(owner)
        return owner
    
class OwnerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)
    phone_number = serializers.CharField(source='user.phone_number', read_only=True)
    role = serializers.CharField(source='user.role', read_only=True)

    brokerage = BrokerageOwnerSerializer(source='brokerage_owners', read_only=True)
    asset_management = AssetManagementOwnerSerializer(source='asset_management_owners', read_only=True)

    class Meta:
        model = BaseOwner
        fields = [
            'owner_name', 'owner_type', 'username', 'email', 'phone_number', 'role', 
            'is_verified_from_legal_team', 'brokerage', 'asset_management'
        ]

class AgreementDocumentSerializer(serializers.ModelSerializer):
    owner = OwnerSerializer(read_only=True)     

    class Meta:
        model = AgreementDocument
        fields = ['id', 'owner', 'document_type', 'document_content', 'created_at', 'status', 'is_verified_from_legal_team']

