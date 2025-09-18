import time
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from location.models import Location
from .serializers import *
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
import requests
from django.conf import settings

from rest_framework.permissions import IsAuthenticated


# Firebase settings
FIREBASE_API_KEY = settings.FIREBASE_API_KEY
FIREBASE_AUTH_URL = f"https://identitytoolkit.googleapis.com/v1/accounts:lookup?key={FIREBASE_API_KEY}"


class CreateOrderView(APIView):
    """
    Create a new Order.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):

        
        print('-----------------i am heere--------------------')
        print('-----------------i am heere--------------------')
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
                customer_instance = Customer.objects.get(user=user)
            except User.DoesNotExist:
                return Response({"error": "User not found"}, status=404)
            except Customer.DoesNotExist:
                return Response({"error": "Customer not found"}, status=404)

            # Deserialize the order data
            data = request.data.copy()
            data["customer"] = customer_instance.id  # Add customer instance ID to the payload
            serializer = OrderSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=201)
            else:
                return Response(serializer.errors, status=400)
        else:
            return Response({"error": "Invalid token"}, status=401)


class UpdateOrderDetailView(APIView):
   
    # need to change code
    def put(self, request, pk):
        Order = get_object_or_404(Order, pk=pk)
        serializer = OrderSerializer(Order, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class OrderDetailView(APIView):
   

    def get(self, request, pk):
        Order = Order.objects.get(id = pk)
        serializer = OrderSerializer(Order)
        
        return Response(serializer.data, status=status.HTTP_200_OK)




class ListOrderView(APIView):
   

    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        
        return Response(serializer.data, status=status.HTTP_200_OK)


class DeleteOrderDetailView(APIView):
   

    def post(self, request, pk):
        Order = get_object_or_404(Order, pk=pk)
        Order.delete()
        # return Response({"message": "Order deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        messages.error(request, "Order deleted successfully.")
        return redirect("getOrderList")





from orders.models import *

class RecentOrders(APIView):
    def get(self, request):

        data = Order.objects.all()

        return render(request, "account/AvenzaAdmin/order.html", {'data' : data})

class TotalOrders(APIView):
    def get(self, request):

        print(request.user)

        data = Order.objects.all()

        return render(request, "account/AvenzaAdmin/order.html", {'data' : data})


def assign_vendor(request, order_id):

    if request.method == "POST":

        order_instance = Order.objects.get(id = order_id)

        vendor_id = request.POST.get('vendor')

        vendor_instance = Vendor.objects.get(id = vendor_id)

        order_instance.ongoing = "ongoing"
        order_instance.vendor = vendor_instance
        order_instance.save()

        return redirect('total_orders')
    
    else:

        order_instance = Order.objects.get(id = order_id)
        vendor_data = Vendor.objects.filter(is_available = True)


        return render(request, "account/AvenzaAdmin/order_detail.html", {'order_instance' : order_instance, 'vendor_data' : vendor_data})

def get_vendor_for_order(request, order_id):

    order_category = Order.objects.filter(id=order_id).values_list('packageId__categories__id', flat=True)
    
    vendor_data = list(Vendor.objects.filter(is_available=True, category__in=order_category).values('id', 'vendorname'))

    print(vendor_data)

    return JsonResponse(vendor_data, safe=False)



def delete_order(request, order_id):


    order_instance = Order.objects.get(id = order_id).delete()



    return redirect('total_orders')


import json
import hashlib
import base64
import requests
import uuid
import logging
import datetime
from django.conf import settings
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse

logger = logging.getLogger('payment')

def generate_tran_id():
    """To genarate a unique order number"""
    uuid_part = str(uuid.uuid4()).split('-')[0].upper()  # Get a part of the UUID
    now = datetime.datetime.now().strftime('%Y%m%d')
    return f"TRX{now}{uuid_part}"

def generate_checksum(data, salt_key, salt_index):
    """To Genarate checksum"""
    checksum_str = data + '/pg/v1/pay' + salt_key
    checksum = hashlib.sha256(checksum_str.encode()).hexdigest() + '###' + salt_index
    return checksum

def home_payment(request):
    if request.method == 'GET':
        return render(request, 'payment_home.html')

@csrf_exempt
def initiate_payment(request):
    if request.method == 'POST':
        """After click pay now it will inisiate payment"""
        amount = request.POST.get('amount') # In rupe
        callback_url = request.build_absolute_uri(reverse('callback'))
        payload = {
            "merchantId": settings.PHONEPE_MERCHANT_ID,
            "merchantTransactionId": generate_tran_id(),
            "merchantUserId": "USR1231",
            "amount": int(amount)*100,  # In paisa
            "redirectUrl": callback_url,
            "redirectMode": "POST",
            "callbackUrl": callback_url,
            "mobileNumber": "9800278886",
            "paymentInstrument": {
                "type": "PAY_PAGE"
            }
        }
        
        data = base64.b64encode(json.dumps(payload).encode()).decode()
        checksum = generate_checksum(data, settings.PHONEPE_MERCHANT_KEY, settings.SALT_INDEX)
        final_payload = {
            "request": data,
        }
        
        headers = {
            'Content-Type': 'application/json',
            'X-VERIFY': checksum,
        }
        
        try:
            print('-------------1---------------')

            response = requests.post(settings.PHONEPE_INITIATE_PAYMENT_URL , headers=headers, json=final_payload)
            print(response)
            data = response.json()
            print(data)

            print('---------------2-------------')

            
            if data['success']:
               
                print('--------------3--------------')
                url = data['data']['instrumentResponse']['redirectInfo']['url']
                print('----------------------------')
                print(url)
                print('----------------------------')
                return redirect(url)
            else:
                return redirect('home_payment')

        except Exception as e:

            print('-----------------------')
            print(e)
            print('-----------------------')
            logger.info("initiate : %s", e)
            return redirect('home_payment')
        

@csrf_exempt
def payment_callback(request):
    if request.method != 'POST':
        logger.error("Invalid request method: %s", request.method)
        return redirect('home_payment')

    try:
        data = request.POST.dict()  # Convert QueryDict to a regular dictionary
        logger.info(data)
        if data.get('checksum') and data.get('code') == "PAYMENT_SUCCESS":
            response = render(request, 'success.html')
            return response
        else:
            logger.info("After payment report:: %s", data)
            return render(request, 'failed.html')
    except Exception as e:
        logger.error("Error parsing request body:: %s", e)
        render(request, 'failed.html')