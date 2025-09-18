from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404

from rest_framework.permissions import AllowAny

from subCategory.models import SubCategory
from .models import HomeBanner, HomeSection
from .serializers import HomeBannerSerializer, HomeSectionSerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from packages.models import Package
from category.models import Category
from location.models import Location


class CreateHomeBannerView(APIView):
    """
    Create a new HomeBanner.
    """

    def get(self, request):
        locations = Location.objects.all()
        return render(request, "createHomeBanner.html", {"locations": locations})

    def post(self, request):
        serializer = HomeBannerSerializer(data=request.data)
        print(request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            messages.success(request, "HomeBanner created successfully!")
            return redirect("createHomeBanner")
        print(serializer.errors)
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        messages.error(request, serializer.data)
        return redirect("createHomeBanner")


class ListHomeBannerView(APIView):
    """
    List all HomeBanners.
    """

    def get(self, request):
        homeBanners = HomeBanner.objects.all()
        serializer = HomeBannerSerializer(homeBanners, many=True)

        # Check if the request is coming from a browser (not API)
        # if request.accepts('text/html'):  # If the request is for HTML content
        return render(request, 'homeBannerList.html', {'homeBanners': serializer.data})

        # If it's an API request (e.g., fetch or AJAX), return JSON response
        # return Response(serializer.data, status=status.HTTP_200_OK)

from rest_framework.permissions import IsAuthenticated

class BannerApiView(APIView):

    permission_classes = [AllowAny]  


    """
    List all HomeBanners as an API endpoint.
    """

    def get(self, request, *args, **kwargs):
        """
        Override the `get` method to return a custom response (optional).
        You can customize how the data is returned or the status code.
        """
        # Fetch the list of HomeBanners
        queryset = HomeBanner.objects.all()

        serializer = HomeBannerSerializer(queryset, many=True)

        # Return the response with status 200
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetHomeBannerDetailView(APIView):
    """
    Retrieve HomeBanner.
    """
    permission_classes = [AllowAny]  


    def get(self, request, pk):
        homeBanner = get_object_or_404(HomeBanner, pk=pk)
        serializer = HomeBannerSerializer(homeBanner)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateHomeBannerDetailView(APIView):
    """
    Update HomeBanner.
    """

    def put(self, request, pk):
        homeBanner = get_object_or_404(HomeBanner, pk=pk)

        # Pass both request.data and request.FILES together
        data = request.data.copy()  # Make a copy of request.data
        data.update(request.FILES)  # Include request.FILES in the data

        # Now, create the serializer with the combined data
        serializer = HomeBannerSerializer(homeBanner, data=data, partial=True)

        if serializer.is_valid():
            serializer.save()
            messages.success(request, "HomeBanner Updated successfully!")
            print('doneeeeeeeeeeeeee')  # Log to verify
            return Response(serializer.data, status=status.HTTP_200_OK)
        print(serializer.errors)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def get(self, request, pk):
        locations = Location.objects.all()
        HomeBanner_instance = HomeBanner.objects.get(id = pk)
        return render(request, "updateHomeBanner.html", {"locations": locations, 'homeBanner_instance' : HomeBanner_instance})

class DeleteHomeBannerDetailView(APIView):
    """
    Update HomeBanner.
    """

    def put(self, request, pk):
        homeBanner = get_object_or_404(HomeBanner, pk=pk)
        homeBanner.delete()
        # return Response({"message": "Location deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        messages.error(request, "HomeBanner deleted successfully.")
        return redirect("getHomeBannerList")


class CreateHomeSectionView(APIView):
    """
    Create a new homeSection.
    """

    def get(self, request):
        packages = Package.objects.all()
        categories = Category.objects.all()
        # subCategories = SubCategory.objects.all()
        locations = Location.objects.all()
        return render(request, "createHomeSection.html", {"packages": packages, "categories": categories
                      , "locations": locations })

    def post(self, request):
        serializer = HomeSectionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            messages.success(request, "HomeSection created successfully!")
            return redirect("createHomeSection")
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        messages.error(request, serializer.data)
        return redirect("createHomeSection")


class ListHomeSectionView(APIView):
    """
    List all homeSections.
    """
    permission_classes = [AllowAny]  

    def get(self, request):
        homeSections = HomeSection.objects.all()
        serializer = HomeSectionSerializer(homeSections, many=True)
        print('hi',serializer.data)
        # Return the response with status 200
        return render(request, 'homeSectionsList.html', {'data': serializer.data})
        # return Response(serializer.data, status=status.HTTP_200_OK)

        
    


class HomeSectionApiView(APIView):
    """
    List all homeSections.
    
    """

    permission_classes = [AllowAny]  


    def get(self, request):
        homeSections = HomeSection.objects.all()
        serializer = HomeSectionSerializer(homeSections, many=True)

        # Return the response with status 200
        # return render(request, 'homeSectionsList.html', {'homeSections': serializer.data})
        return Response(serializer.data, status=status.HTTP_200_OK)

class GetHomeSectionDetailView(APIView):
    """
    Retrieve homeSection.
    """

    def get(self, request, pk):
        homeSection = get_object_or_404(HomeSection, pk=pk)
        serializer = HomeSectionSerializer(homeSection)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateHomeSectionDetailView(APIView):
    """
    Update homeSection.
    """

    def get(self, request, pk):
        # Get the HomeSection by primary key
       
        home_section = get_object_or_404(HomeSection, pk=pk)


        packages = Package.objects.all()
        categories = Category.objects.all()
        # subCategories = SubCategory.objects.all()
        locations = Location.objects.all()
        selected_packages = home_section.packages.values_list('id', flat=True) 

        return render(request, "updateHomeSection.html", {"packages": packages, "categories": categories
                      , "locations": locations, "selected_packages" : list(selected_packages), "home_section" : home_section })

    def put(self, request, pk):
        # Get the HomeSection by primary key
        home_section = get_object_or_404(HomeSection, pk=pk)

        print('----------here--------------')
        # Deserialize and validate the request data
        serializer = HomeSectionSerializer(home_section, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print('----------h3ere--------------')

            messages.success(request, "HomeSection updated successfully!")
            return Response(serializer.data, status=status.HTTP_200_OK)
  # Redirect back to the update page
        # If validation fails, return errors
        messages.error(request, serializer.errors)
        return redirect('updateHomeSection', pk=pk)



class DeleteHomeSectionDetailView(APIView):
    """
    Delete homeSection.
    """

    def get(self, request, pk):
        homeSection = get_object_or_404(HomeSection, pk=pk)
        homeSection.delete()
        # return Response({"message": "HomeSection deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        messages.error(request, "HomeSection deleted successfully.")
        return redirect("getHomeSectionList")
