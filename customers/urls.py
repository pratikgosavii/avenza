from django.urls import path
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('get/', CustomerListView.as_view(), name='customerList'),
    path('get/<int:pk>/', CustomerDetailView.as_view(), name='customerDetail'),
    # path('send-otp/', SendOTPView.as_view(), name='send_otp'),
    # path('verify-otp/', VerifyOTPView.as_view(), name='verify_otp'),
    path("profile/", UserProfileView.as_view(), name="profile"),
    path('register/', CustomerRegisterView.as_view(), name='customerRegister'),
    path('login/', CustomerLoginView.as_view(), name='customerLogin'),
    path('logout/', logout_view, name='customerlogout'),
    # path('customers/login/', FirebaseLoginView.as_view(), name='customerLogin'),
    path('update/<int:pk>/', CustomerUpdateView.as_view(), name='customerUpdate'),
    path('delete/<int:pk>/', CustomerDeleteView.as_view(), name='customerDelete'),

    path('past-order', PastOrders.as_view(), name='past_orders'),

    
    path('create-ticket/', TicketCreateView.as_view(), name='ticket-create'),


    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


    #admin use

    path('update-customer/<int:customer_id>/', update_customer, name='update_customer'),

]
