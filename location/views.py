from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from .models import Location
from .serializers import LocationSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from orders.models import Order
from location.models import Location
from vendors.models import Vendor
from customers.models import Customer
from rest_framework.permissions import AllowAny

class CreateLocationView(APIView):
    """
    Create a new location.
    """

    def get(self, request):
        return render(request, "createLocation.html")

    def post(self, request):
        serializer = LocationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            messages.success(request, "Location created successfully!")
            return redirect("createLocation")
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        messages.error(request, serializer.data)
        return redirect("createLocation")


class ListLocationView(APIView):
    """
    List all locations.
    """

    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return render(request, 'locationsList.html', {'locations': serializer.data})


class LocationDetailsView(APIView):
    """
    View for detailed location data including orders, customers, and vendors.
    """

    def get(self, request, id):
        # Fetch the location details
        location = get_object_or_404(Location, id=id)

        # Fetch related data
        orders = Order.objects.filter(locationId=location)
        customers = Customer.objects.filter(location=location)
        vendors = Vendor.objects.filter(location=location)

        # Prepare data for rendering
        context = {
            'location': {
                'id': location.id,
                'title': location.title,
                'icon': location.image if location.image else None,
            },
            'orders': [{'id': order.id, 'total_amount': order.total_amount} for order in orders],
            'customers': [{'id': customer.id, 'name': customer.user.username} for customer in customers],
            'vendors': [{'id': vendor.id, 'name': vendor.vendorname} for vendor in vendors],
            'order_count': orders.count(),
            'customer_count': customers.count(),
            'vendor_count': vendors.count(),
        }
        print(context)

        return render(request, 'locationsDetails.html', context)


class GetAllLocationView(APIView):
    """
    List all locations.
    """

    permission_classes = [AllowAny]  


    def get(self, request):
        locations = Location.objects.all()
        serializer = LocationSerializer(locations, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
        # return render(request, 'locationsList.html', {'locations': serializer.data})


class GetLocationDetailView(APIView):
    """
    Retrieve location.
    """

    permission_classes = [AllowAny]  

    def get(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        serializer = LocationSerializer(location)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateLocationDetailView(APIView):
    """
    Update location.
    """

    def put(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        serializer = LocationSerializer(location, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    
    def get(self, request, pk):

        location = Location.objects.get(id = pk)

        return render(request, "updateLocation.html", {'location' : location})

class DeleteLocationDetailView(APIView):
    """
    Update location.
    """

    def post(self, request, pk):
        location = get_object_or_404(Location, pk=pk)
        location.delete()
        # return Response({"message": "Location deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        messages.error(request, "Location deleted successfully.")
        return redirect("getLocationList")
