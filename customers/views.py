

from .models import Customer
from admins.models import User
from location.models import Location
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import make_password



    

class CustomerRegisterView(APIView):
    def post(self, request):
        # Get data from the request
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        location_id = request.data.get('location')
        customer_phone_number = request.data.get('customerPhoneNumber')
        date_of_birth = request.data.get('dateOfBirth')
        gender = request.data.get('gender')
        address1 = request.data.get('address1')
        address2 = request.data.get('address2')

        # Validate the password confirmation
        if password != password2:
            return JsonResponse({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if username or email already exists
        if User.objects.filter(username=username).exists():
            return JsonResponse({"error": "This username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return JsonResponse({"error": "This email is already registered."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate phone number
        if Customer.objects.filter(customerPhoneNumber=customer_phone_number).exists():
            return JsonResponse({"error": "This phone number is already registered."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate if location exists
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return JsonResponse({"error": "Invalid location."}, status=status.HTTP_400_BAD_REQUEST)

        # Create User object
        user = User.objects.create(username=username, email=email, role=User.CUSTOMER)
        user.password = make_password(password)  # Hash the password
        user.save()

        # Create Customer object
        customer = Customer.objects.create(
            user=user,
            location=location,
            customerPhoneNumber=customer_phone_number,
            dateOfBirth=date_of_birth,
            gender=gender,
            address1=address1,
            address2=address2
        )

        return JsonResponse({"message": "Customer registered successfully!", "customer_id": customer.id}, status=status.HTTP_201_CREATED)



from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
from django.contrib.auth.hashers import make_password
from .models import Customer, User, Location

class CustomerUpdateView(APIView):
    def get(self, request, pk):
        try:
            # Retrieve the customer
            customer = Customer.objects.select_related('user', 'location').get(id=pk)
            locations = Location.objects.all()  # Get all locations for dropdown

            # Pass the customer and locations to the template
            return render(request, 'updateCustomer.html', {'data': customer, 'locations': locations})
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

    def post(self, request, pk):
        try:
            customer = Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Retrieve form data and set default values if not provided
        username = request.POST.get('username', customer.user.username)
        email = request.POST.get('email', customer.user.email)
        password = request.POST.get('password', None)  # Password is optional
        password2 = request.POST.get('password2', None)  # Confirm password is optional
        customer_phone_number = request.POST.get('customerPhoneNumber', customer.customerPhoneNumber)
        date_of_birth = request.POST.get('dateOfBirth', customer.dateOfBirth)
        gender = request.POST.get('gender', customer.gender)
        address1 = request.POST.get('address1', customer.address1)
        address2 = request.POST.get('address2', customer.address2)

        # If password is provided, validate it
        if password and password != password2:
            return JsonResponse({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Validate uniqueness of username, email, and phone number
        if User.objects.filter(username=username).exclude(id=customer.user.id).exists():
            return JsonResponse({"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST)
        if User.objects.filter(email=email).exclude(id=customer.user.id).exists():
            return JsonResponse({"error": "Email already registered."}, status=status.HTTP_400_BAD_REQUEST)
        if Customer.objects.filter(customerPhoneNumber=customer_phone_number).exclude(id=pk).exists():
            return JsonResponse({"error": "Phone number already registered."}, status=status.HTTP_400_BAD_REQUEST)

        # Update user details if changed
        customer.user.username = username
        customer.user.email = email
        if password:  # Update password only if provided
            customer.user.set_password(password)
        customer.user.save()

        # Update customer fields
        customer.customerPhoneNumber = customer_phone_number

        # Handle date_of_birth to ensure it only updates if a valid date is provided
        if date_of_birth:
            try:
                # Try to parse the date to ensure it's in the correct format (YYYY-MM-DD)
                customer.dateOfBirth = date_of_birth
            except ValueError:
                return JsonResponse({"error": "Invalid date format. It must be in YYYY-MM-DD format."}, status=status.HTTP_400_BAD_REQUEST)

        # Update other fields if provided
        customer.gender = gender if gender else customer.gender
        customer.address1 = address1 if address1 else customer.address1
        customer.address2 = address2 if address2 else customer.address2

        # Save the customer with updated information
        customer.save()
    
        return JsonResponse({"message": "Customer updated successfully!"}, status=status.HTTP_200_OK)
    

class CustomerDeleteView(APIView):
    def post(self, request, pk):
        try:
            customer = Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Delete the associated User object (cascade delete should handle Customer deletion)
        user = customer.user
        user.delete()

        return JsonResponse({"message": "Customer deleted successfully."}, status=status.HTTP_200_OK)

class CustomerListView(APIView):
    def get(self, request):
        customers = Customer.objects.all()
        customer_list = []

      
        # return JsonResponse({"customers": customer_list}, status=status.HTTP_200_OK)
        return render(request, "CustomersList.html", {"customers": customers})


class CustomerDetailView(APIView):
    def get(self, request, pk):
        try:
            customer = Customer.objects.get(id=pk)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        customer_data = {
            "id": customer.id,
            "username": customer.user.username,
            "email": customer.user.email,
            "location": customer.location.name,
            "phone_number": customer.customerPhoneNumber,
            "date_of_birth": customer.dateOfBirth,
            "gender": customer.gender,
            "address1": customer.address1,
            "address2": customer.address2,
        }

        return JsonResponse(customer_data, status=status.HTTP_200_OK)




# import firebase_admin
# from firebase_admin import credentials, auth
# from django.http import JsonResponse
# import json
# from django.views.decorators.csrf import csrf_exempt
# from django.views import View
# import os
# from django.conf import settings

# # Initialize Firebase app if not already initialized
# if not firebase_admin._apps:
#     cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS)
#     firebase_admin.initialize_app(cred)

# class SendOTPView(View):
#     @csrf_exempt
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             phone_number = data.get('phone_number')

#             # Initiate Firebase phone number authentication
#             verification_id = auth.generate_sign_in_with_phone_number_link(phone_number, None)

#             return JsonResponse({'verification_id': verification_id}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)


# class VerifyOTPView(View):
#     @csrf_exempt
#     def post(self, request):
#         try:
#             data = json.loads(request.body)
#             phone_number = data.get('phone_number')
#             otp = data.get('otp')
#             verification_id = data.get('verification_id')

#             # Verify the OTP using Firebase
#             credential = auth.PhoneAuthProvider.credential(verification_id, otp)

#             # Verify the OTP and get the user
#             user = auth.sign_in_with_credential(credential)
#             return JsonResponse({'message': 'OTP verified successfully', 'user_id': user.uid}, status=200)

#         except Exception as e:
#             return JsonResponse({'error': str(e)}, status=400)



from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.views import APIView
from rest_framework.response import Response
import requests


from rest_framework import status

# from rest_framework.permissions import IsAuthenticated

#code to login using google

class CustomerLoginView(APIView):
    def post(self, request):

        id_token = request.data.get('idToken')  # Adjust based on your frontend
        if not id_token:
            return Response({"error": "ID token is required"}, status=400)

        user = register_user(id_token)

        if user:


            return Response({"message": "User authenticated successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid token or user not found"}, status=status.HTTP_401_UNAUTHORIZED)

#code to verify user using token common for all type of login using firebase
from django.conf import settings
from django.contrib.auth.models import User

from admins.forms import *

# Firebase settings
FIREBASE_API_KEY = settings.FIREBASE_API_KEY
FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"


def verify_token(token):
    """Verify the Firebase token and return the user data."""
    headers = {"Content-Type": "application/json"}
    payload = {"idToken": token}
    response = requests.post(FIREBASE_AUTH_URL, headers=headers, json=payload)

    if response.status_code == 200:
        return response.json()["users"][0]
    return None




def register_user(user_data):
    """Register a user based on Firebase token data."""
    firebase_uid = user_data["localId"]
    email = user_data.get("email", None)
    name = user_data.get("displayName", "No Name")

    # Check if user already exists
    if User.objects.filter(username=firebase_uid).exists():
        return None, "A user with this username already exists, try logging in."

    # Prepare data for the form
    form_data = {
        'username': firebase_uid,
        'email': email,
        'first_name': name.split(" ")[0],
        'last_name': " ".join(name.split(" ")[1:]),
    }

    # Create user using the form
    form = UserForm(form_data)
    if form.is_valid():
        user = form.save()
        return user, None
    return None, form.errors



from rest_framework.permissions import AllowAny


class CustomerLoginView(APIView):
    """Handle Firebase Google Login for Users."""

    permission_classes = [AllowAny]  


    def post(self, request):
        id_token = request.data.get("idToken")  # Adjust based on your frontend
        if not id_token:
            return Response({"error": "ID token is required"}, status=400)

        # Verify the Firebase token
        user_data = verify_token(id_token)
        if not user_data:
            return Response({"error": "Invalid ID token"}, status=401)

        # Check or register the user
        firebase_uid = user_data["localId"]

        try:
            user = User.objects.get(username=firebase_uid)
        except User.DoesNotExist:
            user, error = register_user(user_data)

            if user:
                Customer.objects.create(user = user)
            if error:
                return Response({"error": error}, status=400)

        # Log the user in
        user.backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user)

        return Response({"message": "User authenticated successfully"}, status=200)


from django.contrib.auth import logout


def logout_view(request):
    logout(request)  # Logs out the user and clears the session
    return JsonResponse({"message": "User logged out successfully"}, status=200)


from orders.serializers import *

class PastOrders(APIView):
    def get(self, request):
        token = request.headers.get("Authorization", "").split("Bearer ")[-1]

        if not token:
            return Response({"error": "Token is required"}, status=401)


        # Verify token with Firebase
        headers = {"Content-Type": "application/json"}
        payload = {"idToken": token}
        response = requests.post(FIREBASE_AUTH_URL, headers=headers, json=payload)

        if response.status_code == 200:
            
            # Extract user data from Firebase response
            user_data = response.json()["users"][0]
            firebase_uid = user_data["localId"]

            try:
                # Get the corresponding Django user
                user = User.objects.get(username=firebase_uid)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
                    
            orders = Order.objects.filter(customer__user = user)
            serializer = OrderSerializer(orders, many=True)
            # return Response(serializer.data, status=status.HTTP_200_OK)
            
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({"error": "Invalid token"}, status=401)
    

class RecentOrders(APIView):
    def get(self, request):
        # user = verify_token_and_get_user(request)  # Authenticate user
        # if not user:
        #     return JsonResponse({"error": "Session expired please login again"}, status=400)


        # # Fetch orders linked to this user
        # orders = Order.objects.filter(user=user)
        # orders_data = [{"id": o.id, "details": o.details} for o in orders]  # Adjust according to your Order model
        # return JsonResponse({"orders": orders_data}, status=200)
        return JsonResponse({"orders": 'abcd'}, status=200)



from rest_framework.permissions import IsAuthenticated

from admins.serializers import *

class UserProfileView(APIView):

    def get(self, request):

        print('-----------------i am heere--------------------')
        print('-----------------i am heere--------------------')
        token = request.headers.get("Authorization", "").split("Bearer ")[-1]

        if not token:
            return Response({"error": "Token is required"}, status=401)

        # Verify token using Firebase REST API
        headers = {"Content-Type": "application/json"}
        payload = {"idToken": token}

        response = requests.post(FIREBASE_AUTH_URL, headers=headers, json=payload)

        if response.status_code == 200:
            user_data = response.json()["users"][0]
            firebase_uid = user_data["localId"]

            # Get or create the Django user
            try:
                user = User.objects.get(username=firebase_uid)
                customer_instance =  Customer.objects.get(user = user)

            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)

            # If user exists, return profile data
            return Response({"username": user.username, "email": user.email, "customer" : customer_instance.id}, status=200)





# class FirebaseLoginWithPhoneView(APIView):

#     def post(self, request):
#         firebase_token = request.data.get('firebase_token')

#         if not firebase_token:
#             return Response({"error": "Firebase token is required."}, status=status.HTTP_400_BAD_REQUEST)

#         try:
#             decoded_token = auth.verify_id_token(firebase_token)
#             phone_number = decoded_token.get('phone_number')

#             if not phone_number:
#                 return Response({"error": "Invalid Firebase token."}, status=status.HTTP_400_BAD_REQUEST)

#             # Authenticate the customer based on the phone number
#             customer = Customer.objects.filter(customerPhoneNumber=phone_number).first()
#             if not customer:
#                 return Response({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

#             # Return successful response
#             return Response({
#                 "message": "Login successful!",
#                 "data": {
#                     "username": customer.user.username,
#                     "email": customer.user.email,
#                     "customerPhoneNumber": customer.customerPhoneNumber
#                 }
#             }, status=status.HTTP_200_OK)

#         except FirebaseError as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)



from .models import Ticket, Customer

class TicketCreateView(APIView):
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        order_id = request.data.get('order')
        customer_id = request.data.get('customer')
        issue_description = request.data.get('issue_description')
        status = request.data.get('status', 'open')  # Default to 'open'
        
        # Handle image upload
        image = request.FILES.get('image')

        # Validate input data
        if not customer_id:
            return JsonResponse({'error': 'Customer ID is required.'}, status=400)
        if not order_id:
            return JsonResponse({'error': 'Order ID is required.'}, status=400)
        if not issue_description:
            return JsonResponse({'error': 'Issue description is required.'}, status=400)

        try:
            # Get the customer instance
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({'error': f'Customer with ID {customer_id} does not exist.'}, status=404)

        try:
            # Get the order instance
            order = Order.objects.all()
            print(order)
            order = Order.objects.get(customer=customer_id, id=order_id)
        except Order.DoesNotExist:
            return JsonResponse({'error': f'Order with ID {order_id} for customer ID {customer_id} does not exist.'}, status=404)

        try:
            # Fetch the User instance for the vendor
            vendor = Vendor.objects.get(id=order.vendor_id)  
            vendor = vendor.user# Assuming the User model is used for vendors
        except User.DoesNotExist:
            return JsonResponse({'error': f'Vendor with ID {order.vendor_id} does not exist.'}, status=404)

        try:
            # Create a new Ticket instance
            ticket = Ticket.objects.create(
                order_id=order_id,
                customer=customer,
                vendor=vendor,
                issue_description=issue_description,
                image=image,
                status=status,
            )

            return JsonResponse({'message': 'Ticket created successfully.', 'ticket_id': ticket.id}, status=201)

        except Exception as e:
            # Log the error for debugging (optional: you can log this to a file or monitoring tool)
            return JsonResponse({'error': f'An unexpected error occurred: {str(e)}'}, status=400)



# admin use

def update_customer(request, customer_id):

    if request.method == "POST":
            
        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found."}, status=status.HTTP_404_NOT_FOUND)

        # Get the data from the request
        username = request.data.get('username', customer.user.username)
        email = request.data.get('email', customer.user.email)
        password = request.data.get('password')
        password2 = request.data.get('password2')
        location_id = request.data.get('location', customer.location.id)
        customer_phone_number = request.data.get('customerPhoneNumber', customer.customerPhoneNumber)
        date_of_birth = request.data.get('dateOfBirth', customer.dateOfBirth)
        gender = request.data.get('gender', customer.gender)
        address1 = request.data.get('address1', customer.address1)
        address2 = request.data.get('address2', customer.address2)

        # Validate password if provided
        if password and password != password2:
            return JsonResponse({"error": "Passwords do not match."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the username or email is already taken
        if User.objects.filter(username=username).exclude(id=customer.user.id).exists():
            return JsonResponse({"error": "This username is already taken."}, status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exclude(id=customer.user.id).exists():
            return JsonResponse({"error": "This email is already registered."}, status=status.HTTP_400_BAD_REQUEST)

        # Check if the phone number is already registered
        if Customer.objects.filter(customerPhoneNumber=customer_phone_number).exclude(id=customer_id).exists():
            return JsonResponse({"error": "This phone number is already registered."}, status=status.HTTP_400_BAD_REQUEST)

        # Update user
        customer.user.username = username
        customer.user.email = email
        if password:
            customer.user.password = make_password(password)
        customer.user.save()

        # Validate location
        try:
            location = Location.objects.get(id=location_id)
        except Location.DoesNotExist:
            return JsonResponse({"error": "Invalid location."}, status=status.HTTP_400_BAD_REQUEST)

        # Update Customer
        customer.location = location
        customer.customerPhoneNumber = customer_phone_number
        customer.dateOfBirth = date_of_birth
        customer.gender = gender
        customer.address1 = address1
        customer.address2 = address2
        customer.save()

        return JsonResponse({"message": "Customer updated successfully!", "customer_id": customer.id}, status=status.HTTP_200_OK)

    else:

        return render(request, 'update_customer.html', {'data' : Customer.objects.get(id = customer_id)})
        