from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import *


urlpatterns = [
    path('get/', VendorListView.as_view(), name='vendorList'),
    path('register/', VendorRegisterView.as_view(), name='vendorRegister'),
    path('adminRegister/', AdminVendorRegisterView.as_view(), name='adminVendorRegister'),
    path('get/<int:pk>/', VendorDetailView.as_view(), name='vendorDetail'),
    path('update/<int:pk>/', VendorUpdateView.as_view(), name='vendorUpdate'),
    path('delete/<int:pk>/', VendorDeleteView.as_view(), name='vendorDelete'),
    path('approval/<int:pk>/', VendorApprovalView.as_view(), name='vendorApproval'),
    path('login/', VendorLoginView.as_view(), name='vendorLogin'),
    path('dashboard/', VendorDashboardView.as_view(), name='vendorDashboard'),
    path('logout/', VendorLogoutView.as_view(next_page="vendorLogin"), name='vendorLogout'),
    path('VendorTicket/', VendorTicket.as_view(), name='VendorTicket'),
    path('vendor-tickets/filter/', VendorTicketFilter.as_view(), name='VendorTicketFilter'),

    path('vendor-calendar/', vendor_calendar, name='vendor_calendar'),

    path('vendor-request/', VendorRequestView.as_view(), name='vendor_request'),
    path('vendor_profile/<int:vendor_id>/', VendorProfileView.as_view(), name='vendor_profile'),
    path('Feedbacks/', VendorFeedbacks.as_view(), name='VendorFeedback'),

    path('orders/', VendorOders.as_view(), name='VendorOders'),
    path('order-completed/<pk>', VendorOrderCompleted.as_view(), name='VendorOrderCompleted'),
    
    path('payments/', VendorPayments.as_view(), name='VendorPayments'),
    # path('services/', CreateServices.as_view(), name='CreateServices'),
    # path('services-list/', ServicesList.as_view(), name='ServicesList'),
    path('vendor-details/', VendorDetails.as_view(), name='VendorDetails'),
    path('update-vendor-availability/', UpdateVendorAvailability.as_view(), name='update_vendor_availability'),


    
]
