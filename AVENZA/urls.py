from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib import admin

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', admin.site.urls),
    path('api/admins/', include('admins.urls')),
    path('api/categories/', include("category.urls")),
    path('api/customers/', include('customers.urls')),
    path('api/homePage/', include('homePage.urls')),
    path('api/locations/', include('location.urls')),
    path('api/notifications/', include("notifications.urls")),
    path('api/orders/', include("orders.urls")),
    path('api/packages/', include("packages.urls")),
    path('api/subCategories/', include("subCategory.urls")),
    path('api/vendors/', include('vendors.urls')),
    # get and refresh the token for the authentication
    path('token/', TokenObtainPairView.as_view(), name='token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='tokenRefresh')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
