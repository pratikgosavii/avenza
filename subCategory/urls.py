from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import (
      CreateSubCategoryView,
      ListSubCategoryView,
      GetSubCategoryDetailView,
      UpdateSubCategoryDetailView,
      DeleteSubCategoryDetailView,
      ListSubCategoryLocationView,
      SubCategoryApiView

)

urlpatterns = [
      # Other URL patterns
      path('create/', CreateSubCategoryView.as_view(), name='createSubCategory'),
      path('get/', ListSubCategoryView.as_view(), name='getSubCategoryList'),
      path('subcategory-get/', SubCategoryApiView.as_view(), name='getSubCategoryList'),

      
      path('get/location/<int:pk>/', ListSubCategoryLocationView.as_view(), name='getSubCategoryLocationList'),
      path('get/<int:pk>/', GetSubCategoryDetailView.as_view(), name='getSubCategoryDetail'),
      path('update/<int:pk>/', UpdateSubCategoryDetailView.as_view(), name='updateSubCategoryDetail'),
      path('delete/<int:pk>/', DeleteSubCategoryDetailView.as_view(), name='deleteSubCategory'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
