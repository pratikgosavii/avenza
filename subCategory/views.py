from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from location.models import Location
from category.models import Category
from .models import SubCategory
from .serializers import SubCategorySerializer
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse


class CreateSubCategoryView(APIView):
    """
    Create a new subCategory.
    """

    def get(self, request):
        locations = Location.objects.all()
        categories = Category.objects.all()
        return render(request, "createSubCategory.html", {"locations": locations, "categories": categories})

    def post(self, request):
        serializer = SubCategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            # return Response(serializer.data, status=status.HTTP_201_CREATED)
            messages.success(request, "SubCategory created successfully!")
            return redirect("createSubCategory")
        # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        messages.error(request, serializer.data)
        return redirect("createSubCategory")


class ListSubCategoryView(APIView):
    """
    List all subCategories.
    """

    def get(self, request):
        subCategories = SubCategory.objects.all()
        serializer = SubCategorySerializer(subCategories, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return render(request, 'subCategoriesList.html', {'subCategories': serializer.data})
    


class SubCategoryApiView(APIView):
    """
    List subcategories filtered by both location and category.
    """

    def get(self, request):
        # Get location IDs from the query parameters (multiple possible)
        location_ids = request.GET.getlist('location_id')  
        category_ids = request.GET.getlist('category_id')  

        # If both location and category filters are provided
        if location_ids and category_ids:
            subCategories = SubCategory.objects.filter(
                location__id__in=location_ids,
                category__id__in=category_ids
            )
        # If only location filter is provided
        elif location_ids:
            subCategories = SubCategory.objects.filter(location__id__in=location_ids)
        # If only category filter is provided
        elif category_ids:
            subCategories = SubCategory.objects.filter(category__id__in=category_ids)
        else:
            # If neither location nor category filter is provided, return all subcategories
            subCategories = SubCategory.objects.all()

        # Serialize the filtered subcategories
        serializer = SubCategorySerializer(subCategories, many=True)

        # Return the serialized data as a JSON response
        return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)

        # return render(request, 'subCategoriesList.html', {'subCategories': serializer.data})


class GetSubCategoryDetailView(APIView):
    """
    Retrieve subCategory.
    """

    def get(self, request, pk):
        subCategory = get_object_or_404(SubCategory, pk=pk)
        serializer = SubCategorySerializer(subCategory)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateSubCategoryDetailView(APIView):
    """
    Update subCategory.
    """

    def put(self, request, pk):
        subCategory = get_object_or_404(SubCategory, pk=pk)
        serializer = SubCategorySerializer(subCategory, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteSubCategoryDetailView(APIView):
    """
    Update subCategory.
    """

    def post(self, request, pk):
        subCategory = get_object_or_404(SubCategory, pk=pk)
        subCategory.delete()
        # return Response({"message": "SubCategory deleted successfully."}, status=status.HTTP_204_NO_CONTENT)
        messages.error(request, "SubCategory deleted successfully.")
        return redirect("getSubCategoryList")


class ListSubCategoryLocationView(APIView):
    """
    Get categories filtered by location.
    """

    def get(self, request, pk):
        # Get location by ID
        location = Location.objects.get(id=pk)
        # Get categories related to the location
        subCategories = SubCategory.objects.filter(location=location)
        # Serialize categories and send response
        categories_data = [{"id": subCategory.id, "title": subCategory.title} for subCategory in subCategories]
        return Response(categories_data, status=status.HTTP_200_OK)

