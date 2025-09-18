from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import AdminListCreateView, AdminRetrieveUpdateDestroyView
from .views import AdminDashboardView, AdminLoginView,AdminLogoutView
from .views import *

urlpatterns = [
    # Admin dashboard and login/logout
    path('login/', AdminLoginView.as_view(), name='adminLogin'),
    path('dashboard/', AdminDashboardView.as_view(), name='adminDashboard'),
    path('logout/', AdminLogoutView.as_view(next_page="adminLogin"), name='adminLogout'),
    
    path('why-avenza/', why_avenza_add, name='why_avenza'),  # create or fetch list of admins
    path('get-avenza/', GetAvenza.as_view(), name='get_avenza'), 

    path('add-testimonials/', add_testimonials, name='add_testimonials'),  # create or fetch list of admins
    path('update-testimonials/<testimonials_id>', update_testimonials, name='update_testimonials'),  # create or fetch list of admins
    path('list-testimonials/', list_testimonials, name='list_testimonials'),  # create or fetch list of admins
    path('delete-testimonials/<testimonials_id>', delete_testimonials, name='delete_testimonials'),  # create or fetch list of admins
    path('get-testimonials/', Gettestimonials.as_view(), name='get_testimonials'), 

    path('add-cancelation_policy/', add_cancelation_policy, name='add_cancelation_policy'),  # create or fetch list of admins
    path('update-cancelation_policy/<cancelation_policy_id>', update_cancelation_policy, name='update_cancelation_policy'),  # create or fetch list of admins
    path('list-cancelation_policy', list_cancelation_policy, name='list_cancelation_policy'),  # create or fetch list of admins
    path('delete-cancelation_policy/<cancelation_policy_id>', delete_cancelation_policy, name='delete_cancelation_policy'),  # create or fetch list of admins
    path('get-cancelation-policy/', Getcancelation_policy.as_view(), name='get_cancelation_policy'), 

    path('listCreate/', AdminListCreateView.as_view(), name='adminListCreate'),  # create or fetch list of admins
    # retrieve update or delete admin on the basis of id
    path('retrieveUpdateDestroy/<int:pk>/', AdminRetrieveUpdateDestroyView.as_view(), name='adminDetail'),

    path('update-customer/<int:pk>/', update_customer, name='update_customer'),
    path('delte-customer/<int:pk>/', delete_customer, name='delete_customer'),

]
