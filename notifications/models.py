# models.py
from django.db import models
from django.contrib.auth import get_user_model
from admins.models import User
from vendors.models import Vendor


class Notification(models.Model):
    ACTION_CHOICES = [
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    action = models.CharField(max_length=10, choices=ACTION_CHOICES, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.user}"
