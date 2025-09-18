from rest_framework import serializers
from .models import *
from location.models import Location
from location.serializers import LocationSerializer
from packages.serializers import CustomizationSerializer


class OrderCustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCustomization
        fields = ['customization', 'quantity']  # Specify the fields to accept input for

class OrderSerializer(serializers.ModelSerializer):
    
    customizations = OrderCustomizationSerializer(many=True, read_only=False)  # For creation only

    class Meta:
        model = Order
        fields = [
            'date', 'slot', 'packageId', 'locationId', 'vendor', 'customer',
            'shipping_address', 'pincode', 'city', 'contact_no', 'total_amount',
            'customizations',  # Include the customizations for input
        ]

    def create(self, validated_data):
        # Extract and remove customizations from validated data
        customizations_data = validated_data.pop('customizations', [])

        # Create the order instance
        order = Order.objects.create(**validated_data)

        # Create related OrderCustomization instances
        for customization_data in customizations_data:
            OrderCustomization.objects.create(order=order, **customization_data)

        return order


    def update(self, instance, validated_data):
        # Update all fields directly
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
