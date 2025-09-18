from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import (
      CreateCategoryView,
      ListCategoryView,
      GetCategoryDetailView,
      UpdateCategoryDetailView,
      DeleteCategoryDetailView,
      ListCategoryLocationView,
      CategoryViewApi

)

urlpatterns = [
      # Other URL patterns
      path('create/', CreateCategoryView.as_view(), name='createCategory'),
      path('get/', ListCategoryView.as_view(), name='getCategoryList'),

      path('category-get/', CategoryViewApi.as_view(), name='getCatego'),
      
      path('get/location/<int:pk>/', ListCategoryLocationView.as_view(), name='getCategoryLocationList'),
      path('get/<int:pk>/', GetCategoryDetailView.as_view(), name='getCategoryDetail'),
      path('update/<int:pk>/', UpdateCategoryDetailView.as_view(), name='updateCategoryDetail'),
      path('delete/<int:pk>/', DeleteCategoryDetailView.as_view(), name='deleteCategory'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

