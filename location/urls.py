from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import (
      CreateLocationView,
      ListLocationView,
      GetLocationDetailView,
      UpdateLocationDetailView,
      DeleteLocationDetailView,
      GetAllLocationView,
      LocationDetailsView

)

urlpatterns = [
      # Other URL patterns
      path('create/', CreateLocationView.as_view(), name='createLocation'),
      path('get/', ListLocationView.as_view(), name='getLocationList'),
      path('location-details/<int:id>/', LocationDetailsView.as_view(), name='LocationDetailsView'),
      path('get-location/', GetAllLocationView.as_view(), name='getLocationListsdsd'),
      
      path('get/<int:pk>/', GetLocationDetailView.as_view(), name='getLocationDetail'),
      path('update/<int:pk>/', UpdateLocationDetailView.as_view(), name='updateLocationDetail'),
      path('delete/<int:pk>/', DeleteLocationDetailView.as_view(), name='deleteLocation'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
