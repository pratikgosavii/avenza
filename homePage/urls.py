from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import (
      CreateHomeBannerView,
      ListHomeBannerView,
      GetHomeBannerDetailView,
      UpdateHomeBannerDetailView,
      DeleteHomeBannerDetailView,
      CreateHomeSectionView,
      ListHomeSectionView,
      GetHomeSectionDetailView,
      UpdateHomeSectionDetailView,
      DeleteHomeSectionDetailView,
      BannerApiView,
      HomeSectionApiView
)
urlpatterns = [
      # HomeBanner URLs
      path('homeBanner/create/', CreateHomeBannerView.as_view(), name='createHomeBanner'),
      path('homeBanner/get/', ListHomeBannerView.as_view(), name='getHomeBannerList'),

      path('get-homeBanner/', BannerApiView.as_view(), name='getHomeBannerListsds'),

      path('homeBanner/get/<int:pk>/', GetHomeBannerDetailView.as_view(), name='getHomeBannerDetail'),
      path('homeBanner/update/<int:pk>/', UpdateHomeBannerDetailView.as_view(), name='updateHomeBannerDetail'),
      path('homeBanner/delete/<int:pk>/', DeleteHomeBannerDetailView.as_view(), name='deleteHomeBanner'),
      # HomeSection URLs
      path('homeSection/create/', CreateHomeSectionView.as_view(), name='createHomeSection'),
      path('homeSection/get/', ListHomeSectionView.as_view(), name='getHomeSectionList'),

      path('get-homeSection/', HomeSectionApiView.as_view(), name='getHomeSectionListasasas'),

      path('homeSection/get/<int:pk>/', GetHomeSectionDetailView.as_view(), name='getHomeSectionDetail'),
      path('homeSection/update/<int:pk>/', UpdateHomeSectionDetailView.as_view(), name='updateHomeSectionDetail'),
      path('homeSection/delete/<int:pk>/', DeleteHomeSectionDetailView.as_view(), name='deleteHomeSection'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
