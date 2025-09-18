from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
      # Other URL patterns
      path('create/', CreatePackageView.as_view(), name='createPackage'),
      path('update/<pk>', UpdatePackageView.as_view(), name='updatePackage'),
      path('get/', ListPackageView.as_view(), name='getPackageList'),

      path('get-package/', PackageApiView.as_view(), name='getPackageListsdsdsdsd'),
      
      # path('get-package-details/<pk>', PackageDetailsApiView.as_view(), name='getPackageDetailsList'),

      path('add-customize/', CustomizeAddApiView.as_view(), name='add_customize'),
      path('update-customize/<pk>', CustomizeUpdateApiView.as_view(), name='update_customize'),
      path('delte-customize/<pk>', CustomizeDelteApiView.as_view(), name='delete_customize'),
      path('get-customize/', CustomizeGetApiView.as_view(), name='get_customize'),

      path('add-package-inclusion/', add_package_inclusion, name='add_package_inclusion'),  # create or fetch list of admins
      path('update-package-inclusion/<package_inclusion_id>', update_package_inclusion, name='update_package_inclusion'),  # create or fetch list of admins
      path('list-package-inclusion/', list_package_inclusion, name='list_package_inclusion'),  # create or fetch list of admins
      path('delete-package-inclusion/<package_inclusion_id>', delete_package_inclusion, name='delete_package_inclusion'),  # create or fetch list of admins
      path('get-package-inclusion/', Getpackage_inclusion.as_view(), name='get_package_inclusion'), 
      
      path('add-need-to-know/', add_need_to_know, name='add_need_to_know'),  # create or fetch list of admins
      path('update-need-to-know/<need_to_know_id>', update_need_to_know, name='update_need_to_know'),  # create or fetch list of admins
      path('list-need-to-know/', list_need_to_know, name='list_need_to_know'),  # create or fetch list of admins
      path('delete-need-to-know/<need_to_know_id>', delete_need_to_know, name='delete_need_to_know'),  # create or fetch list of admins
      path('get-need-to-know/', Getneed_to_know.as_view(), name='get_need_to_know'), 

      path('get/location/<int:pk>/', ListPackageLocationView.as_view(), name='getPackageLocationList'),
      path('get/<int:pk>/<int:location_id>/', GetPackageDetailView.as_view(), name='getPackageDetail'),
      path('delete/<int:pk>/', DeletePackageDetailView.as_view(), name='deletePackage'),
      path('update/<int:pk>/', UpdatePackageDetailView.as_view(), name='updatePackageDetail'),



      
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
