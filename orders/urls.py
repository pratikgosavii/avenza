from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from .views import *

urlpatterns = [
      # Other URL patterns
      path('get/', ListOrderView.as_view(), name='getOrderList'),
      path('get/<int:pk>/', OrderDetailView.as_view(), name='OrderDetail'),
      path('create/', CreateOrderView.as_view(), name='createOrder'),
      path('update/<int:pk>/', UpdateOrderDetailView.as_view(), name='updateOrderDetail'),
      path('delete/<int:pk>/', DeleteOrderDetailView.as_view(), name='deleteOrder'),


      # admin urls // dashboard urlss

      path('recent-order', RecentOrders.as_view(), name='recent_orders'),
      path('total-order', TotalOrders.as_view(), name='total_orders'),
      path('order-assign-vendor/<order_id>', assign_vendor, name='assign_vendor'),
      path('get_vendor_for_order/<order_id>', get_vendor_for_order, name='get_vendor_for_order'),
      path('delete-order/<order_id>', delete_order, name='delete_order'),

      path('payment-home', home_payment, name='home_payment'),
      path('payment-initiate', initiate_payment, name='initiate_payment'),
      path('callback', payment_callback, name='callback'),




] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

