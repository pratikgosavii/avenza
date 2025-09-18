#code to verify user using token common for all type of login using firebase
from django.conf import settings
from django.contrib.auth.models import User

from admins.forms import *
import jwt 
import time

# Firebase settings
FIREBASE_API_KEY = settings.FIREBASE_API_KEY
FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"



from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from admins.models import User
import requests
 

class FirebaseAuthentication(BaseAuthentication):
    

    def authenticate(self, request):
        # Extract token from 'Authorization' header
        token = request.headers.get('Authorization')
        if not token:
            return None

        token = token.split(' ')[-1]  # Remove 'Bearer ' prefix
        decoded_token = self.decode_token(token)

        # If the token is expired, attempt to refresh it
        if self.is_token_expired(decoded_token):
            # Extract refresh_token from request data or client storage
            refresh_token = request.data.get("refresh_token")
            if not refresh_token:
                raise AuthenticationFailed("Refresh token is required to refresh the ID token.")
            
            token = self.refresh_token(refresh_token)
            decoded_token = self.decode_token(token)

        # Verify and get user info from Firebase
        return self.verify_user(decoded_token)

    def decode_token(self, token):
        """Decode the Firebase ID token to check its expiration."""
        try:
            decoded_token = jwt.decode(token, options={"verify_signature": False})  # Don't verify signature
            return decoded_token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed("ID token has expired")
        except jwt.DecodeError:
            raise AuthenticationFailed("Invalid ID token")
    
    def is_token_expired(self, decoded_token):
        """Check if the Firebase ID token is expired based on the 'exp' claim."""
        exp_timestamp = decoded_token.get("exp")
        if exp_timestamp and exp_timestamp < time.time():
            return True
        return False

    def refresh_token(self, refresh_token):
        """Use Firebase refresh token to get a new ID token."""
        headers = {"Content-Type": "application/json"}
        payload = {"grant_type": "refresh_token", "refresh_token": refresh_token}
        url = f"https://securetoken.googleapis.com/v1/token?key={FIREBASE_API_KEY}"

        response = requests.post(url, headers=headers, data=payload)

        if response.status_code == 200:
            return response.json()["id_token"]
        else:
            raise AuthenticationFailed("Unable to refresh Firebase token")

    def verify_user(self, decoded_token):
        """Verify the Firebase user and return the corresponding Django user."""
        print('--------------------------------')
        print('--------------------------------')
        print('--------------------------------')
        print(decoded_token.get("user_id"))

        print('--------------------------------')
        print('--------------------------------')
        print('--------------------------------')
        print('--------------------------------')


        """Verify the Firebase user and return the corresponding Django user."""
        firebase_uid = decoded_token.get("user_id")  # Use 'user_id' instead of 'uid'
        if not firebase_uid:
            raise AuthenticationFailed("The token is invalid or malformed. 'user_id' not found.")

        try:
            user = User.objects.get(username=firebase_uid)
            return (user, None)  # Return user and None for authentication context
        except User.DoesNotExist:
            raise AuthenticationFailed("User does not exist")