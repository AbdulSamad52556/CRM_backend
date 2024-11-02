from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password, check_password

class BaseOwner(models.Model):
    OWNER_TYPES = [
        ('Individual', 'Individual'),
        ('Company', 'Company'),
    ]
    AGREEMENT_TYPES = [
        ('Brokerage', 'Brokerage'),
        ('Asset Management', 'Asset Management'),
    ]
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, null=True)
    owner_name = models.CharField(max_length=255)
    owner_type = models.CharField(max_length=50, choices=OWNER_TYPES)
    agreement_type = models.CharField(max_length=50, choices=AGREEMENT_TYPES,null=True)
    is_verified_from_legal_team = models.BooleanField(default=False)

    def __str__(self):
        return self.owner_name
    
    def get_user_data(self):
        if self.user:
            return {
                'username': self.user.username,
                'email': self.user.email,
                'role': self.user.role.name if hasattr(self.user, 'role') else None,
                'phone_number': self.user.phone_number if hasattr(self.user, 'phone_number') else None
            }
        return None

class BrokerageOwner(models.Model):
    owner = models.OneToOneField(BaseOwner, on_delete=models.CASCADE, related_name='brokerage_owners')
    contract_modes = [
        ('percentage_of_sales', 'Percentage of Total Sales'),
        ('lease_commission', 'Lease Commission'),
        ('custom', 'Custom Arrangement'),
    ]
    contract_mode = models.CharField(max_length=50, choices=contract_modes)

class AssetManagementOwner(BaseOwner):
    owner = models.OneToOneField(BaseOwner, on_delete=models.CASCADE, related_name='asset_management_owners',null=True)
    contract_modes = [
        ('property_management', 'Property Management'),
        ('sub_lease', 'Sub-Lease'),
    ]
    contract_mode = models.CharField(max_length=50, choices=contract_modes)
    revenue_type = models.CharField(max_length=50, blank=True, null=True)

class Property(models.Model):
    PROPERTY_TYPES = [
        ('Residential', 'Residential'),
        ('Commercial', 'Commercial'),
    ]

    owner = models.ForeignKey(BaseOwner, on_delete=models.CASCADE, related_name='crm_properties') 
    property_name = models.CharField(max_length=255)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPES)
    property_location = models.CharField(max_length=255) 
    mode = models.CharField(max_length=255) 
    reserved_units = models.IntegerField(default=0)
    available_units = models.IntegerField(default=0)
    taken_units = models.IntegerField(default=0)
    expected_commission = models.DecimalField(max_digits=10, decimal_places=2)
    contract_type = models.CharField(max_length=50)

    def __str__(self):
        return self.property_name

class AgreementDocument(models.Model):
    owner = models.ForeignKey(BaseOwner, on_delete=models.CASCADE)
    document_type = models.CharField(max_length=50, choices=[
        ('Brokerage', 'Brokerage'),
        ('Asset Management', 'Asset Management'),
    ])
    document_content = models.TextField() 
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, choices=[
        ('Pending', 'Pending'),
        ('Verified', 'Verified'),
        ('Sent', 'Sent'),
        ('Signed', 'Signed'),
    ], default='Pending')
    is_verified_from_legal_team = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.document_type} Agreement for {self.owner.owner_name}"