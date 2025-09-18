from rest_framework import serializers
from .models import Vendor, OrderCompletionImage
from admins.models import User
from location.serializers import LocationSerializer
from location.models import Location
from category.models import Category
from packages.models import Package, PackageLocationPrice
# from .models import Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User  # Replace with your actual User model
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        
class VendorSerializerData(serializers.ModelSerializer):
    first_name = serializers.CharField(source='user.first_name', required=True)
    user = UserSerializer()
    email = serializers.CharField(source='user.email', required=True)
    location = serializers.StringRelatedField()
    category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Vendor
        fields = [
            'id',
            'user',
            'first_name',
            'category',
            'vendorname',
            'email',
            'image',
            'location',
            'vendorPhoneNumber',
            'portfolio_link'
        ]


class VendorSerializer(serializers.ModelSerializer):
    # Fields to handle user data
    username = serializers.CharField(source='user.username', required=True)
    email = serializers.EmailField(source='user.email', required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=True)

    # Location field (allows the user to provide a location ID)
    location = serializers.PrimaryKeyRelatedField(queryset=Location.objects.all())

    # Nested location details
    locationDetails = LocationSerializer(source='location', read_only=True)

    # Categories (list of category IDs)
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True, required=False)

    class Meta:
        model = Vendor
        fields = [
            'id', 'username', 'email', 'password', 'password2',
            'vendorname', 'vendorPhoneNumber', 'location',
            'locationDetails', 'categories', 'is_approved', 'is_pending','image'
        ]
        read_only_fields = ['is_approved', 'is_pending']

    # Custom validation logic
    def validate(self, attrs):
        user_data = attrs.get('user', {})
        username = user_data.get('username')
        email = user_data.get('email')
        password = attrs.get('password')
        password2 = attrs.get('password2')

        # Check if the passwords match
        if password and password2 and password != password2:
            raise serializers.ValidationError({"password2": "Passwords do not match."})

        # Check if the username already exists
        if username:
            existing_user = User.objects.filter(username=username).exclude(
                id=self.instance.user.id if self.instance else None).first()
            if existing_user:
                raise serializers.ValidationError({"username": "This username is already taken."})

        # Check if the email already exists
        if email:
            existing_email_user = User.objects.filter(email=email).exclude(
                id=self.instance.user.id if self.instance else None).first()
            if existing_email_user:
                raise serializers.ValidationError({"email": "This email is already registered."})

        return attrs

    # Create method to handle the creation of User and Vendor objects
    def create(self, validated_data):
        # Extract and remove the user data from validated_data
        user_data = validated_data.pop('user', {})
        username = user_data.get('username')
        email = user_data.get('email')
        password = validated_data.pop('password')
        password2 = validated_data.pop('password2')

        # Step 1: Create the User instance
        user = User.objects.create(username=username, email=email,role=User.VENDOR)
        user.set_password(password)  # Securely hash the password
        user.save()  # Save the User instance to the database

        # Step 2: Create the Vendor instance
        location = validated_data.pop('location')  # Extract location from the validated data
        vendorPhoneNumber = validated_data.get('vendorPhoneNumber')  # Get vendorPhoneNumber if provided
        vendorname = validated_data.get('vendorname') 

        # Create the Vendor instance
        vendor = Vendor.objects.create(
            user=user,  # Assign the User instance to the Vendor
            location=location,  # Assign the Location instance to the Vendor
            vendorname=vendorname,  # Vendor name
            vendorPhoneNumber=vendorPhoneNumber,  # Vendor phone number
        )

        categories = validated_data.get('categories', [])
        if categories:
            vendor.category.set(categories)  # Associate the categories to the vendor

        # Return the created Vendor instance
        return vendor


    def update(self, instance, validated_data):
        # Update the User model
        user_data = validated_data.pop('user', {})
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        # Hash password if it is provided
        password = validated_data.pop('password', None)
        if password:
            instance.user.set_password(password)
            instance.user.save()

        # Update the Vendor model
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance



class OrderCompletionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderCompletionImage
        fields = ['id', 'completion_images']

class PackageLocationPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PackageLocationPrice
        fields = ['package', 'category', 'location', 'price']


class PackageSerializer(serializers.ModelSerializer):
    categories = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), many=True)
    package_location_prices = PackageLocationPriceSerializer(many=True)

    class Meta:
        model = Package
        fields = ['title', 'description', 'image', 'is_active', 'categories', 'package_location_prices']

    def create(self, validated_data):
        # Handle creation of PackageLocationPrice instances
        package_location_prices_data = validated_data.pop('package_location_prices')
        package = Package.objects.create(**validated_data)
        
        for price_data in package_location_prices_data:
            PackageLocationPrice.objects.create(package=package, **price_data)
        
        return package


# class ReviewSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Review
#         fields = ['id', 'order', 'rating', 'comment', 'created_at']
#         read_only_fields = ['created_at']  # Make user and created_at read-only

#     def create(self, validated_data):
#         print("hi",validated_data)
#         review = Review.objects.create(**validated_data)
#         return review