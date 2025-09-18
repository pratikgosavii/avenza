from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from location.models import Location
from subCategory.models import SubCategory
from category.models import Category
from .models import Package,Customization,PackageLocationPrice
from .serializers import PackageSerializer,CustomizationSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes



from vendors.decorators import *


@admin_login_required
class CreatePackageView(APIView):
    """
    View to create a new package.
    """

    def get(self, request):
        locations = Location.objects.all()
        categories = Category.objects.all()
        customizations = Customization.objects.all()
        packageinclusion = PackageInclusion.objects.all()
        needtoknow = need_to_know.objects.all()
        return render(request, "createPackage.html", {
            "locations": locations,
            "Categories": categories,
            "customize": customizations,
            "packageinclusion": packageinclusion,
            "need_to_know": needtoknow,
        })

    def post(self, request):
        print(request.data)
        # Extract package data
        title = request.data.get("title")
        description = request.data.get("description")
        short_description = request.data.get("shortDescription")
        categories = request.data.getlist("category")
        locations = request.data.getlist("location")
        package_inclusion = request.data.getlist("package_inclusion")
        needtoknow = request.data.getlist("need_to_know")
        customizations = request.data.getlist("customizations")  # Extract customizations
        prices = [request.data.get(f'price_{i}') for i in range(len(locations))]

        # Save package details
        package_image = request.FILES.get("packageImages")
        package = Package.objects.create(
            title=title,
            description=description,
            short_description=short_description,
            is_active=True,
            image=package_image,
        )

        # # Assign categories and customizations
        package.categories.set(categories)
        package.customizations.set(customizations)  # Assign customizations to the package
        package.package_inclusion.set(package_inclusion)  # Assign customizations to the package
        package.need_to_know.set(needtoknow)  # Assign customizations to the package


        # Save the prices for each combination of category and location
        for i, location_id in enumerate(locations):
            location = Location.objects.get(id=location_id)
            print("Location:", location)  # This will show the location object
            price = prices[i]
            for category_id in categories:
                category = Category.objects.get(id=category_id)
                # print("Category:", category)  # This will show the category object
                PackageLocationPrice.objects.create(
                    package=package,
                    category=category,
                    location=location,
                    price=price
                )

        messages.success(request, "Package created successfully with prices!")
        return redirect("createPackage")
    

    

@admin_login_required
class UpdatePackageView(APIView):
    """
    View to create a new package.
    """

    def get(self, request, pk):
        Package_instance = Package.objects.get(id=pk)

        # Fetch all locations, categories, and customizations
        locations = Location.objects.all()
        categories = Category.objects.all()
        customizations = Customization.objects.all()
        packageinclusion = PackageInclusion.objects.all()
        needtoknow = need_to_know.objects.all()

        # Get associated locations and categories for the package
        location_prices = Package_instance.package_location_prices.values('location_id', 'price')
        associated_location_prices = {item['location_id']: item['price'] for item in location_prices}

        print(associated_location_prices)
        # Get associated categories for the package

        return render(request, "updatePackage.html", {
            "locations": locations,
            "Categories": categories,
            "customize": customizations,
            "packageinclusion": packageinclusion,
            "need_to_know": needtoknow,
            "Package_instance": Package_instance,
            "associated_location_prices": associated_location_prices,  # {location_id: price}
        })




    def post(self, request, pk=None):
        print(request.data)
        
        # Extract package data
        title = request.data.get("title")
        description = request.data.get("description")
        short_description = request.data.get("shortDescription")
        categories = request.data.getlist("category")
        locations = request.data.getlist("location")
        customizations = request.data.getlist("customizations")  # Extract customizations
        prices = [request.data.get(f'price_{i}') for i in range(len(locations))]
        package_inclusion = request.data.getlist("package_inclusion")
        needtoknow = request.data.getlist("need_to_know")

        package_image = request.FILES.get("packageImages")

        # Check if updating an existing package
        if pk:
            package = Package.objects.get(id=pk)
            package.title = title
            package.description = description
            package.image = package_image or package.image  # Keep the old image if no new image provided
            package.save()

            # Update categories and customizations
            package.categories.set(categories)
            package.customizations.set(customizations)
            package.package_inclusion.set(package_inclusion)  # Assign customizations to the package
            package.need_to_know.set(needtoknow)  # Assign customizations to the package

            # Delete all existing `PackageLocationPrice` records for this package
            PackageLocationPrice.objects.filter(package=package).delete()
            for i, location_id in enumerate(locations):
                location = Location.objects.get(id=location_id)
                price = prices[i]
                for category_id in categories:
                    category = Category.objects.get(id=category_id)
                    PackageLocationPrice.objects.create(
                        package=package,
                        category=category,
                        location=location,
                        price=price
                    )

        messages.success(request, "Package updated successfully with prices!")
        return redirect("updatePackage", pk=package.id)

        # else:
        #     # Create a new package if `pk` is not provided
        #     package = Package.objects.create(
        #         title=title,
        #         description=description,
        #         is_active=True,
        #         image=package_image,
        #     )
        #     package.categories.set(categories)
        #     package.customizations.set(customizations)

        # Save the prices for each combination of category and location
        


    # def post(self, request):
    #     print(request.data)
    #     # Extract package data
    #     title = request.data.get("title")
    #     description = request.data.get("description")
    #     short_description = request.data.get("shortDescription")
    #     categories = request.data.getlist("category")
    #     locations = request.data.getlist("location")
    #     customizations = request.data.getlist("customizations")  # Extract customizations
    #     prices = [request.data.get(f'price_{i}') for i in range(len(locations))]

    #     # Save package details
    #     package_image = request.FILES.get("packageImages")
    #     package = Package.objects.create(
    #         title=title,
    #         description=description,
    #         is_active=True,
    #         image=package_image,
    #     )

    #     # # Assign categories and customizations
    #     package.categories.set(categories)
    #     package.customizations.set(customizations)  # Assign customizations to the package


    #     # Save the prices for each combination of category and location
    #     for i, location_id in enumerate(locations):
    #         location = Location.objects.get(id=location_id)
    #         print("Location:", location)  # This will show the location object
    #         price = prices[i]
    #         for category_id in categories:
    #             category = Category.objects.get(id=category_id)
    #             # print("Category:", category)  # This will show the category object
    #             PackageLocationPrice.objects.create(
    #                 package=package,
    #                 category=category,
    #                 location=location,
    #                 price=price
    #             )

    #     messages.success(request, "Package created successfully with prices!")
    #     return redirect("createPackage")
    

    
from django.db.models import Prefetch
@admin_login_required
class ListPackageView(APIView):
    def get(self, request):
        # Fetch all PackageLocationPrice entries first
        location_prices = PackageLocationPrice.objects.select_related('package', 'location', 'category')

        package_data = []

        # Iterate through the location_prices first
        for location_price in location_prices:
            # Prepare the package details for each location_price
            package_info = {
                'id': location_price.package.id,
                'subid': location_price.id,
                'title': location_price.package.title,
                'image': location_price.package.image.url if location_price.package.image else None,
                'description': location_price.package.description,
                'categories': [category.title for category in location_price.package.categories.all()],
                'package_inclusion': [i.title for i in location_price.package.package_inclusion.all()],
                'need_to_know': [i.title for i in location_price.package.need_to_know.all()],
                'location': location_price.location.title,
                'price': location_price.price
            }

            # Add this location_price info to the package_data list
            package_data.append(package_info)


        # Pass the package_data to the template
        return render(request, 'packagesList.html', {'packages': package_data})



@admin_login_required
class CustomizeAddApiView(APIView):
    def get(self, request):
        return render(request, 'addCustomizations.html')

    def post(self, request):
        serializer = CustomizationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Package created successfully!")
        return redirect("add_customize")


@admin_login_required
class CustomizeUpdateApiView(APIView):
    def get(self, request, pk):
        Customization_instnace = Customization.objects.get(id = pk)
        return render(request, 'updateCustomizations.html', {'Customization_instnace' : Customization_instnace})

    def put(self, request, pk):
       
        Customization_instance = get_object_or_404(Customization, pk=pk)

        # Pass both request.data and request.FILES together
        data = request.data.copy()  # Make a copy of request.data
        data.update(request.FILES)  # Include request.FILES in the data

        # Now, create the serializer with the combined data
        serializer = CustomizationSerializer(Customization_instance, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, "HomeBanner Updated successfully!")
            print('doneeeeeeeeeeeeee')  # Log to verify
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)
        return redirect("add_customize")
    


@admin_login_required
class CustomizeDelteApiView(APIView):  
    def get(self, request, pk):
        customization = get_object_or_404(Customization, pk=pk)
        customization.delete()
        # return Response({"message": "Package deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        messages.error(request, "Package deleted successfully.")
        return redirect("get_customize")




@admin_login_required
class CustomizeGetApiView(APIView):
    def get(self, request):
        customizations = Customization.objects.all()
        serializer = CustomizationSerializer(customizations, many=True)
        # return Response(serializer.data)
        return render(request, 'listCustomizations.html',{"customize":serializer.data})





@admin_login_required
class Getpackage_inclusion(APIView):
    
    def get(self, request):
        data = PackageInclusion.objects.all()  # Assuming package_inclusion is the model name

        if not data.exists():
            return JsonResponse({"error": "No data found"}, status=404)

        response_data = []
        for i in data:
            temp = {
                "id": i.id,
                "title": i.title,
            }
            response_data.append(temp)

        return JsonResponse({"data": response_data}, status=200)

from .models import *

@admin_login_required
def add_package_inclusion(request):
    
    if request.method == "POST":

        title = request.POST.get('title')


        instance = PackageInclusion.objects.create(title = title)
        instance.save()

        return redirect('list_package_inclusion')
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_package_inclusion.html')

@admin_login_required
def update_package_inclusion(request, package_inclusion_id):
    
    instance = PackageInclusion.objects.get(id = package_inclusion_id)

    if request.method == "POST":

        title = request.POST.get('title')

        print(title)

        instance.title = title
        instance.save()

        return redirect('list_package_inclusion')
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'update_package_inclusion.html', {'data' : instance})


@admin_login_required
def list_package_inclusion(request):

    data = PackageInclusion.objects.all()

    return render(request, 'list_package_inclusion.html', {'data' : data})


@admin_login_required
def delete_package_inclusion(request, package_inclusion_id):

    data = PackageInclusion.objects.get(id = package_inclusion_id).delete()

    return redirect('list_package_inclusion')




class Getneed_to_know(APIView):
    def get(self, request):
        data = need_to_know.objects.all()  # Assuming need_to_know is the model name

        if not data.exists():
            return JsonResponse({"error": "No data found"}, status=404)

        response_data = []
        for i in data:
            temp = {
                "id": i.id,
                "title": i.title,
            }
            response_data.append(temp)

        return JsonResponse({"data": response_data}, status=200)

from .models import *

@admin_login_required
def add_need_to_know(request):
    
    if request.method == "POST":

        title = request.POST.get('title')


        instance = need_to_know.objects.create(title = title)
        instance.save()

        return redirect('list_need_to_know')
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'add_need_to_know.html')

@admin_login_required
def update_need_to_know(request, need_to_know_id):
    
    instance = need_to_know.objects.get(id = need_to_know_id)

    if request.method == "POST":

        title = request.POST.get('title')

        print(title)

        instance.title = title
        instance.save()

        return redirect('list_need_to_know')
    
    else:

        # create first row using admin then editing only

        

        return render(request, 'update_need_to_know.html', {'data' : instance})


@admin_login_required
def list_need_to_know(request):

    data = need_to_know.objects.all()

    return render(request, 'list_need_to_know.html', {'data' : data})


@admin_login_required
def delete_need_to_know(request, need_to_know_id):

    data = need_to_know.objects.get(id = need_to_know_id).delete()

    return redirect('list_need_to_know')





class PackageApiView(APIView):

    permission_classes = [AllowAny]  

    """
    List all packages filtered by location_id.
    """

    def get(self, request):
        # Get location_id and category_id from query parameters
        location_id = request.query_params.getlist('location_id', None)  # Use getlist to get multiple values
        category_id = request.query_params.getlist('category_id', None)

        print('------------------------')
        print(location_id)
        print(category_id)

        # Initialize location_prices
        location_prices = PackageLocationPrice.objects.select_related('package', 'location', 'category')

        # Filter location_prices based on location_id and category_id if provided
        if location_id and location_id[0]:  # Check if location_id is provided and not empty
            # If there's a single string with multiple values, split it into separate integers
            try:
                location_ids = [int(val.strip()) for val in location_id[0].split(',') if val.strip()]
            except ValueError:
                return Response({"error": "Invalid location ID format."}, status=status.HTTP_400_BAD_REQUEST)

            # Only filter if we have valid IDs
            if location_ids:
                location_prices = location_prices.filter(location_id__in=location_ids)

        if category_id and category_id[0]:  # Check if category_id is provided and not empty
            try:
                category_ids = [int(val.strip()) for val in category_id[0].split(',') if val.strip()]
            except ValueError:
                return Response({"error": "Invalid category ID format."}, status=status.HTTP_400_BAD_REQUEST)

            # Only filter if we have valid IDs
            if category_ids:
                location_prices = location_prices.filter(category_id__in=category_ids)

        package_data = []

        # Iterate through the filtered location_prices
        for location_price in location_prices:
            # Fetch customizations related to the package
            customizations = location_price.package.customizations.all()
            customization_data = [
                {
                    "id": customization.id,
                    "title": customization.title,
                    "price": str(customization.price),
                    "image": customization.image.url if customization.image else None,
                    "description": customization.description,
                }
                for customization in customizations
            ]

            package_inclusion = location_price.package.package_inclusion.all()
            customization_data = [
                {
                    "id": i.id,
                    "title": i.title,
                    
                }
                for i in package_inclusion
            ]

            need_to_know = location_price.package.need_to_know.all()
            need_to_know_data = [
                {
                    "id": i.id,
                    "title": i.title,
                    
                }
                for i in need_to_know
            ]

            # Prepare the package details for each location_price
            package_info = {
                'id': location_price.package.id,
                'title': location_price.package.title,
                'image': location_price.package.image.url if location_price.package.image else None,
                'description': location_price.package.description,
                'categories': [category.title for category in location_price.package.categories.all()],
                'location': location_price.location.title,
                'price': str(location_price.price),  # Convert price to string for JSON serialization
                'customizations': customization_data,  # Include customization details
                'package_inclusion': customization_data,  # Include customization details
                'need_to_know': need_to_know_data,  # Include customization details
            }

            # Add this package_info to the package_data list
            package_data.append(package_info)

        return Response(package_data, status=status.HTTP_200_OK)




# @permission_classes([IsAuthenticated])
class GetPackageDetailView(APIView):
    """
    Retrieve package.
    """

    permission_classes = [AllowAny]  # This allows unauthenticated access to this view


    def get(self, request, pk, location_id):
        # Get location_id from query parameters

        # Filter location_prices based on location_id if provided
        if pk:
            location_prices = PackageLocationPrice.objects.get(package=pk, location__id = location_id)


            customizations_data = [
                {
                    'id': customization.id,
                    'title': customization.title,
                    'price': str(customization.price),  # Convert price to string
                    'image': customization.image.url if customization.image else None,
                    'description': customization.description,
                }
                for customization in location_prices.package.customizations.all()
            ]

            package_inclusion = location_prices.package.package_inclusion.all()
            customization_data = [
                {
                    "id": i.id,
                    "title": i.title,
                    
                }
                for i in package_inclusion
            ]

            need_to_know = location_prices.package.need_to_know.all()
            need_to_know_data = [
                {
                    "id": i.id,
                    "title": i.title,
                    
                }
                for i in need_to_know
            ]


            
            # Prepare the package details for each location_price
            package_info = {
                'id': location_prices.package.id,
                'title': location_prices.package.title,
                'image': [location_prices.package.image.url if location_prices.package.image else None],
                'description': location_prices.package.description,
                'short_description': location_prices.package.short_description,
                'categories': [category.title for category in location_prices.package.categories.all()],
                'location': location_prices.location.title,
                'price': str(location_prices.price),  # Convert price to string for JSON serialization
                'customizations': customizations_data, 
                'package_inclusion': customization_data,  # Include customization details
                'need_to_know': need_to_know_data,  
            }
            

            # Add this package_info to the package_data list

            return Response(package_info, status=status.HTTP_200_OK)
        else:

            return Response({"error": "id missing"}, status=401)


class UpdatePackageDetailView(APIView):
    """
    Update package.
    """

    permission_classes = [AllowAny]  # This allows unauthenticated access to this view

    def put(self, request, pk):
        print("hi")
        try:
            package = Package.objects.get(pk=pk)
        except Package.DoesNotExist:
            return Response({"error": "Package not found"}, status=status.HTTP_404_NOT_FOUND)

        # Update package fields
        package.title = request.data.get("title", package.title)
        package.description = request.data.get("description", package.description)

        # Update package image if provided
        package_image = request.FILES.get("packageImages")
        if package_image:
            package.image = package_image

        package.save()

        # Update categories
        categories = request.data.getlist("categories")
        if categories:
            package.categories.set(categories)

        # Update customizations
        customizations = request.data.getlist("customizations")
        if customizations:
            package.customizations.set(customizations)

        # Update prices
        locations = request.data.getlist("locations")
        prices = request.data.get("prices")  # Assume prices is a dictionary: {"location_id": {"category_id": "price"}}

        # Delete old prices and add new ones
        PackageLocationPrice.objects.filter(package=package).delete()
        for location_id, category_prices in prices.items():
            location = Location.objects.get(id=location_id)
            for category_id, price in category_prices.items():
                category = Category.objects.get(id=category_id)
                PackageLocationPrice.objects.create(
                    package=package,
                    location=location,
                    category=category,
                    price=price
                )

        serializer = PackageSerializer(package)
        return Response(serializer.data, status=status.HTTP_200_OK)


@admin_login_required
class DeletePackageDetailView(APIView):
    """
    Update package.
    """

    def post(self, request, pk):
        package = get_object_or_404(PackageLocationPrice, pk=pk)
        package.delete()
        # return Response({"message": "Package deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        messages.error(request, "Package deleted successfully.")
        return redirect("getPackageList")


class ListPackageLocationView(APIView):
    """
    Get packages filtered by location.
    """

    def get(self, request, pk):
        # Get location by ID
        location = Location.objects.get(id=pk)
        # Get categories related to the location
        packages = Package.objects.filter(location=location)
        # Serialize categories and send response
        packages_data = [{"id": package.id, "title": package.title} for package in packages]
        return Response(packages_data, status=status.HTTP_200_OK)
