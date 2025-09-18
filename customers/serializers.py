from rest_framework import serializers
from .models import Customer
from admins.models import User
from location.serializers import LocationSerializer
from location.models import Location


class CustomerSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', required=True)
    email = serializers.EmailField(source='user.email', required=True)
    password = serializers.CharField(write_only=True, required=True)
    password2 = serializers.CharField(write_only=True, required=False)

    location = serializers.PrimaryKeyRelatedField(
        queryset=Location.objects.all()
    )  # Accepts Location ID for creating/updating and fetches the instance automatically

    locationDetails = LocationSerializer(source='location', read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id', 'username', 'email', 'password', 'password2',
            'location', 'locationDetails', 'customerPhoneNumber', 
            'dateOfBirth', 'gender', 'address1', 'address2'
        ]
        read_only_fields = ['id']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')

        # Check if passwords match
        if password and password2 and password != password2:
            raise serializers.ValidationError({"password2": "Passwords do not match."})

        # Check if the username is already taken
        username = attrs.get('user', {}).get('username')
        if username:
            existing_user = User.objects.filter(username=username).exclude(
                id=self.instance.user.id if self.instance else None).first()
            if existing_user:
                raise serializers.ValidationError({"username": "This username is already taken."})

        # Check if the email is already taken
        email = attrs.get('user', {}).get('email')
        if email:
            existing_email_user = User.objects.filter(email=email).exclude(
                id=self.instance.user.id if self.instance else None).first()
            if existing_email_user:
                raise serializers.ValidationError({"email": "This email is already registered."})

        # Validate unique customer phone number
        customerPhoneNumber = attrs.get('customerPhoneNumber')
        if customerPhoneNumber:
            existing_phoneNumber_customer = Customer.objects.filter(customerPhoneNumber=customerPhoneNumber).exclude(
                id=self.instance.id if self.instance else None).first()
            if existing_phoneNumber_customer:
                raise serializers.ValidationError({"phoneNumber": "This PhoneNumber is already registered."})

        return attrs

    def create(self, validated_data):
        # Extract user data
        user_data = validated_data.pop('user')
        username = user_data.get('username')
        email = user_data.get('email')
        password = validated_data.pop('password')

        # Create the User instance
        user = User.objects.create(username=username, email=email, role=User.CUSTOMER)
        user.set_password(password)  # Set password securely
        user.save()

        # Create the Customer instance
        customer = Customer.objects.create(user=user, **validated_data)
        return customer

from .models import Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ['order', 'customer', 'user', 'issue_description', 'image', 'status']
