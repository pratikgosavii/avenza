# views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Notification
from admins.models import User
from django.shortcuts import get_object_or_404
from vendors.models import Vendor

# User = get_user_model()
class AdminNotificationListView(APIView):
    """
    Get all unread notifications for the admin dashboard.
    """
    def get(self, request):
        # Get the notifications for admins
        admin = request.user  # Assume the request is made by the admin user

        if admin.role != User.ADMIN:
            return Response({"error": "You are not authorized to view this."}, status=status.HTTP_403_FORBIDDEN)

        notifications = Notification.objects.filter(user=admin, read=False)
        notification_data = [{
            "id": notification.id,
            "vendor": notification.vendor.business_name,
            "message": notification.message,
            "created_at": notification.created_at,
        } for notification in notifications]

        return Response(notification_data, status=status.HTTP_200_OK)

class VendorApprovalView(APIView):
    """
    Admin approves or rejects a vendor.
    """
    def post(self, request, pk):
        action = request.data.get("action")
        if action not in ['approve', 'reject']:
            return Response({"error": "Invalid action. Use 'approve' or 'reject'."}, status=status.HTTP_400_BAD_REQUEST)

        # Get the vendor to be approved/rejected
        vendor = get_object_or_404(Vendor, id=pk)

        # Check if the vendor is pending
        if vendor.is_pending:
            if action == 'approve':
                vendor.is_approved = True
                vendor.is_pending = False
            else:  # reject
                vendor.delete()  # Delete the vendor if rejected

            vendor.save()

            # Update the notification for the vendor
            notification = Notification.objects.get(vendor=vendor, user__role=User.ADMIN, read=False)
            notification.action = action
            notification.read = True
            notification.save()

            return Response({
                "message": f"Vendor {action}d successfully."
            }, status=status.HTTP_200_OK)

        return Response({"error": "Vendor is already approved or rejected."}, status=status.HTTP_400_BAD_REQUEST)
