# urls.py
from django.urls import path
from .views import AdminNotificationListView, VendorApprovalView

urlpatterns = [
    path('get', AdminNotificationListView.as_view(), name='admin-notifications'),
    path('approve/vendor/<int:pk>', VendorApprovalView.as_view(), name='vendor-approval'),
]