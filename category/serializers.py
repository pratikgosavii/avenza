from rest_framework import serializers
from .models import *
from location.models import Location
from location.serializers import LocationSerializer



class BannerImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryBannerImage
        fields = ['id', 'image']


class CategorySerializer(serializers.ModelSerializer):
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), many=True)
    locationDetails = LocationSerializer(source='location', read_only=True, many=True)

    banner_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=True),
        write_only=True
    )
    banner_images_read = serializers.SerializerMethodField()  # Read-only field for banner images

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'sub_title_category',
            'description',
            'locationDetails',  # Used for creating/updating using Location ID
            'icon',
            'category_image',
            'is_active',
            'location',
            'created_at',
            'updated_at',
            'banner_images',       # Write-only for file uploads
            'banner_images_read',  # Read-only for retrieving image URLs
        ]

    def get_banner_images_read(self, obj):
        # Fetch and serialize related banner images for read operations
        return [
            {
                "id": banner.id,
                "url": banner.image.url,
            }
            for banner in CategoryBannerImage.objects.filter(category=obj)
        ]

    
    def create(self, validated_data):
        banner_images_data = validated_data.pop('banner_images', [])
        locations = validated_data.pop('location', [])
        category = Category.objects.create(**validated_data)
        category.location.set(locations)

        # Save banner images
        for image_data in banner_images_data:
            CategoryBannerImage.objects.create(category=category, image=image_data)

        return category

    def update(self, instance, validated_data):
        banner_images_data = validated_data.pop('banner_images', None)
        locations = validated_data.pop('location', [])

        # Update the instance fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update Many-to-Many location field
        instance.location.set(locations)

        # Update banner images if provided
        if banner_images_data:
            # Clear existing images and add new ones
            CategoryBannerImage.objects.filter(category=instance).delete()
            for image_data in banner_images_data:
                CategoryBannerImage.objects.create(category=instance, image=image_data)

        return instance

