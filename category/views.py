from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from location.models import Location
from .models import Category
from .serializers import CategorySerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from rest_framework.permissions import AllowAny



class CreateCategoryView(APIView):
    """
    Create a new category.
    """

    def get(self, request):
        locations = Location.objects.all()
        return render(request, "createCategory.html", {"locations": locations})

    def post(self, request):

        print(request.data)

        serializer = CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            messages.success(request, "Category created successfully!")
            return redirect("createCategory")
        print(serializer.errors)
        # Log errors to the console
        print("Validation Errors:", serializer.errors)
        
        error_messages = "; ".join([f"{field}: {', '.join(errors)}" for field, errors in serializer.errors.items()])
        messages.error(request, f"Failed to create category: {error_messages}")
        return redirect("createCategory")


class ListCategoryView(APIView):
    """
    List all categories.
    """

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        print(serializer.data)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return render(request, 'categoriesList.html', {'categories': serializer.data})

class CategoryViewApi(APIView):
    """
    List all categories.
    """
    permission_classes = [AllowAny]  

    def get(self, request):
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        # return render(request, 'categoriesList.html', {'categories': serializer.data})
        return JsonResponse({"categories": serializer.data}, status=status.HTTP_200_OK)


class GetCategoryDetailView(APIView):
    """
    Retrieve category.
    """

    permission_classes = [AllowAny]  


    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from vendors.decorators import *

class UpdateCategoryDetailView(APIView):
    """
    Update category.
    """
    permission_classes = [AllowAny]  # This allows unauthenticated access to this view


    def get(self, request, pk):
        locations = Location.objects.all()
        category_instance = Category.objects.get(id = pk)
        serializer = CategorySerializer(category_instance)
        print(serializer.data)
        return render(request, "updateCategory.html", {"locations": locations, "category_instance" : serializer.data})
    

    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
    def put(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        serializer = CategorySerializer(category, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    

class DeleteCategoryDetailView(APIView):
    """
    Update category.
    """

    def get(self, request, pk):
        category = get_object_or_404(Category, pk=pk)
        category.delete()
        # return Response({"message": "Category deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        messages.error(request, "Category deleted successfully.")
        return redirect("getCategoryList")


class ListCategoryLocationView(APIView):
    """
    Get categories filtered by location.
    """
    permission_classes = [AllowAny]  

    def get(self, request, pk):
        # Get location by ID
        location = Location.objects.get(id=pk)
        print(location)
        # Get categories related to the location
        categories = Category.objects.filter(location=location)
        print(categories)
        # Serialize categories and send response
        categories_data = [{"id": category.id, "title": category.title} for category in categories]
        return Response(categories_data, status=status.HTTP_200_OK)

