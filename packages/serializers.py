from rest_framework import serializers
from .models import Package,Customization
from location.models import Location
from location.serializers import LocationSerializer
from subCategory.models import SubCategory
from category.models import Category
from subCategory.serializers import SubCategorySerializer
from category.serializers import CategorySerializer



# class PackageSerializer(serializers.ModelSerializer):
#     location = serializers.PrimaryKeyRelatedField(
#         queryset=Location.objects.all()
#     )  # Accepts Location ID for creating/updating and fetches the instance automatically

#     # Add a nested location serializer for retrieving location details
#     locationDetails = LocationSerializer(source='location', read_only=True)

#     # Many-to-many relation for subCategories
#     Categories = serializers.PrimaryKeyRelatedField(
#         queryset=Category.objects.all(), many=True
#     )  # Accepts multiple subCategories IDs for creating/updating

#     # Nested serializer for category details on retrieval
#     CategoriesDetails = CategorySerializer(source='Categories', read_only=True, many=True)

#     class Meta:
#         model = Package
#         fields = [
#             'id', 'title', 'description', 'image', 'price', 'is_active',
#             'location',  # Used for creating/updating using Location ID
#             'locationDetails',  # Provides full location details during retrieval
#             'Categories',  # Used for creating/updating using subCategories ID
#             'CategoriesDetails',  # Provides full subCategories details during retrieval
#             'created_at',
#             'updated_at',
#         ]
#         read_only_fields = ['created_at', 'updated_at']

#     def create(self, validated_data):
#         # Remove 'Categories' from the validated data, since it's a Many-to-Many field
#         subCategories_data = validated_data.pop('Categories', [])

#         # Create the Package instance
#         package = Package.objects.create(**validated_data)

#         # Assign the subCategories (ManyToManyField) separately after the Package instance is created
#         package.subCategories.set(subCategories_data)  # Use .set() to assign multiple related objects

#         return package

#     def update(self, instance, validated_data):
#         # Remove 'subCategories' from validated_data since it's a Many-to-Many field
#         subCategories_data = validated_data.pop('subCategories', None)

#         # Update all fields directly (except for ManyToManyField)
#         for attr, value in validated_data.items():
#             setattr(instance, attr, value)

#         # Save the instance first
#         instance.save()

#         # If 'subCategories' was provided, update the Many-to-Many relationship
#         if subCategories_data is not None:
#             instance.subCategories.set(subCategories_data)  # Update Many-to-Many relationship

#         return instance


from rest_framework import serializers
from .models import Package

class PackageSerializer(serializers.ModelSerializer):
    # Serialize the categories field as a list of related category titles (or IDs)
    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='title'  # Change 'title' to the desired field in Category
    )

    class Meta:
        model = Package
        fields = [
            'id', 
            'title', 
            'description', 
            'short_description', 
            'image', 
            'is_active', 
            'categories', 
            'created_at', 
            'updated_at'
        ]


class CustomizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customization
        fields = '__all__'


