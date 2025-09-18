from rest_framework import serializers
from .models import Location


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ['id', 'title', 'description', 'image', 'is_active', 'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    # Image validation
    def validate_image(self, value):
        if value and not value.name.endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError("Only JPG, JPEG, or PNG image formats are supported.")
        return value

    def create(self, validated_data):
        # Perform any custom logic before creating the object
        # For example, logging, processing data, etc.
        location = Location.objects.create(**validated_data)
        # Additional actions can be performed here
        return location

    def update(self, instance, validated_data):
        # Update all fields directly
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
