from rest_framework import serializers
from category.models import Category
from category.serializers import CategorySerializer
from location.models import Location
from location.serializers import LocationSerializer
from .models import SubCategory


class SubCategorySerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all()
    )  # Accepts Location ID for creating/updating and fetches the instance automatically

    # Add a nested category serializer for retrieving category details
    locationDetails = LocationSerializer(source='location', read_only=True)
    # category detail
    category = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all()
    )  # Accepts category ID for creating/updating and fetches the instance automatically

    # Add a nested category serializer for retrieving category details
    categoryDetails = CategorySerializer(source='category', read_only=True)

    class Meta:
        model = Category
        fields = [
            'id', 'title', 'description', 'is_active',
            'location',  # Used for creating/updating using Location ID
            'locationDetails',  # Provides full location details during retrieval
            'category',  # Used for creating/updating using category ID
            'categoryDetails',  # Provides full category details during retrieval
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # No need to pop the location and category; DRF handles it as an instance
        return SubCategory.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # Update all fields directly
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
