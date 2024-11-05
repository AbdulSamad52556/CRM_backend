# serializers.py
from rest_framework import serializers
from .models import Property, PropertyImage, Unit

class PropertyImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PropertyImage
        fields = ['image']

class PropertySerializer(serializers.ModelSerializer):
    property_images = PropertyImageSerializer(many=True, required=False)
    
    class Meta:
        model = Property
        fields = [
            'id','property_name', 'property_type', 'mode', 'area_name', 'google_maps_link', 
            'zone_number', 'street_number', 'building_number', 'available_units', 
            'contract_type', 'payment_file', 'property_images', 'owner_id'
        ]

    def create(self, validated_data):
        try:
            images_data = self.context['request'].FILES.getlist('property_images')
            property_instance = Property.objects.create(**validated_data)

            for image_data in images_data:
                PropertyImage.objects.create(property=property_instance, image=image_data)

            return property_instance
        except Exception as e:
            print(e, 'serializer error')
            raise serializers.ValidationError("Error creating property with images.")

class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = [
            'id','property', 'unit_no', 'unit_type', 'size_sqm', 'furnished', 'floor_no', 'bedrooms',
            'parking_spaces', 'water_connection_no', 'electricity_connection_no', 'cooling_number',
            'rental_price', 'sales_price', 'status', 'layout_type'
        ]