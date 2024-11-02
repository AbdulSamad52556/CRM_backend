from django.db import models
from crm.models import BaseOwner

class Property(models.Model):
    SALES_MODE = 'sales'
    LEASING_MODE = 'leasing'

    PROPERTY_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
    ]
    CONTRACT_TYPES = [
        ('Exclusive', 'Exclusive'),
        ('Non-Exclusive', 'Non-Exclusive'),
    ]
    
    property_name = models.CharField(max_length=255)
    property_type = models.CharField(max_length=50, choices=PROPERTY_TYPE_CHOICES)
    mode = models.CharField(max_length=20, choices=[
        (SALES_MODE, 'Sales'),
        (LEASING_MODE, 'Leasing'),
    ])
    owner = models.ForeignKey(BaseOwner, on_delete=models.CASCADE, related_name='asset_management_properties', null=True)
    area_name = models.CharField(max_length=100)
    google_maps_link = models.URLField()
    zone_number = models.CharField(max_length=50)
    street_number = models.CharField(max_length=50)
    building_number = models.CharField(max_length=50)
    reserved_units = models.PositiveIntegerField(default=0)
    available_units = models.PositiveIntegerField()
    taken_units = models.PositiveIntegerField(default=0)
    contract_type = models.CharField(max_length=50, choices=CONTRACT_TYPES, null=True)
    expected_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    generated_commission = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    payment_file = models.FileField(upload_to='payment_plans/',null=True,blank=True)
    def __str__(self):
        return self.property_name

class PropertyImage(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='property_images/')

class Unit(models.Model):
    UNIT_STATUS_CHOICES = [
        ('available', 'Available'),
        ('reserved', 'Reserved'),
        ('sold', 'Sold'),
        ('rented', 'Rented'),
    ]
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='units')
    unit_no = models.CharField(max_length=50)
    unit_type = models.CharField(max_length=50)  # Studio, 1BR, 2BR, etc.
    size_sqm = models.DecimalField(max_digits=6, decimal_places=2)
    furnished = models.BooleanField(default=False)
    floor_no = models.IntegerField()
    bedrooms = models.PositiveIntegerField()
    parking_spaces = models.PositiveIntegerField(default=0)
    water_connection_no = models.CharField(max_length=100, blank=True, null=True)
    electricity_connection_no = models.CharField(max_length=100, blank=True, null=True)
    cooling_number = models.CharField(max_length=100, blank=True, null=True)
    rental_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sales_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    status = models.CharField(max_length=20, choices=UNIT_STATUS_CHOICES, default='available')
    layout_type = models.CharField(max_length=50)
    marketing_kit = models.TextField()  # Could include links or references to media resources

    def __str__(self):
        return f"{self.property.property_name} - Unit {self.unit_no}"

class Commission(models.Model):
    EXCLUSIVE_CONTRACT = 'exclusive'
    NON_EXCLUSIVE_CONTRACT = 'non-exclusive'
    
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='commissions')
    unit = models.ForeignKey(Unit, on_delete=models.CASCADE, null=True, blank=True)
    contract_type = models.CharField(max_length=20, choices=[
        (EXCLUSIVE_CONTRACT, 'Exclusive'),
        (NON_EXCLUSIVE_CONTRACT, 'Non-Exclusive'),
    ])
    expected_commission = models.DecimalField(max_digits=10, decimal_places=2)
    generated_commission = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.property.property_name} - {self.contract_type} Commission"
