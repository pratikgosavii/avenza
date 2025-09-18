from rest_framework import serializers
from .models import HomeBanner, HomeSection
from packages.models import Package
from packages.serializers import PackageSerializer
from category.models import Category
from category.serializers import CategorySerializer
from location.models import Location
from location.serializers import LocationSerializer
from subCategory.models import SubCategory
from subCategory.serializers import SubCategorySerializer


class HomeBannerSerializer(serializers.ModelSerializer):

    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), many=True)
    locationDetails = LocationSerializer(source='location', read_only=True, many=True)
    # Accepts Location ID for creating/updating and fetches the instance automatically

    # Add a nested location serializer for retrieving location details

    class Meta:
        model = HomeBanner
        fields = ['id', 'title', 'description', 'image', 'is_active',
                  'location',
                    'locationDetails',  # Used for creating/updating using Location ID
                  'created_at', 'updated_at']
        read_only_fields = ['created_at', 'updated_at']

    # Image validation
    def validate_image(self, value):
        if value and not value.name.endswith(('.jpg', '.jpeg', '.png')):
            raise serializers.ValidationError("Only JPG, JPEG, or PNG image formats are supported.")
        return value

    def create(self, validated_data):
        locations = validated_data.pop('location', [])
        homeBanner = HomeBanner.objects.create(**validated_data)
        homeBanner.location.set(locations)
        return homeBanner

    def update(self, instance, validated_data):
        # Update all fields directly
          # Update the 'location' field correctly as it's a ManyToManyField
        locations = validated_data.pop('location', None)  # Get locations from validated data
        
        # Update all other fields directly
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()

        # Update the 'location' ManyToManyField
        if locations is not None:
            instance.location.set(locations)  # Set the new locations for the instance

        return instance


class HomeSectionSerializer(serializers.ModelSerializer):
    # Many-to-many relation for categories
    categories = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(), many=True
    )  # Accepts multiple Category IDs for creating/updating

    categoriesDetail = CategorySerializer(source='categories', read_only=True, many=True)

    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all(), many=True)
    locationDetails = LocationSerializer(source='location', read_only=True, many=True)

    # Nested serializer for category details on retrieval
    # Many-to-many relation for packages
    packages = serializers.PrimaryKeyRelatedField(
        queryset=Package.objects.all(), many=True
    )  # Accepts multiple Package IDs for creating/updating

    # Nested serializer for package details on retrieval
    packagesDetail = PackageSerializer(source='packages', read_only=True, many=True)


    class Meta:
        model = HomeSection
        fields = [
            'id', 'title', 'description', 'image', 'is_active',
            'categories',  # Used for creating/updating using Category IDs
            'categoriesDetail',  # Provides full categories details during retrieval
            'packages',  # Used for creating/updating using Package IDs
            'packagesDetail',  # Provides full packages detail during retrieval
            'location',  # Used for creating/updating using Location ID
            'locationDetails',  # Provides full location details during retrieval
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at', 'updated_at']

    def create(self, validated_data):
        # Create a new HomeSection instance and add the related categories and packages
        categories_data = validated_data.pop('categories')
        packages_data = validated_data.pop('packages')
        print(validated_data)
        locations = validated_data.pop('location', [])


        home_section = HomeSection.objects.create(**validated_data)

        # Add categories and packages to the instance
        home_section.categories.set(categories_data)
        home_section.packages.set(packages_data)
        home_section.location.set(locations)
        home_section.save()

        return home_section

    def update(self, instance, validated_data):
        # Update the HomeSection instance with the provided data
        categories_data = validated_data.pop('categories', None)
        packages_data = validated_data.pop('packages', None)
        locations = validated_data.pop('location', [])

        # Update the basic fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
 # Update Many-to-Many location field
        instance.location.set(locations)
        # If categories or packages were provided, update them
        if categories_data is not None:
            instance.categories.set(categories_data)

        if packages_data is not None:
            instance.packages.set(packages_data)

        instance.save()
        return instance
