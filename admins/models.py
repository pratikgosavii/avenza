from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ADMIN = 'admin'
    VENDOR = 'vendor'
    CUSTOMER = 'customer'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (VENDOR, 'Vendor'),
        (CUSTOMER, 'Customer'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=ADMIN, null=True, blank=True)
    is_verified = models.BooleanField(default=False)  # Optional: For email verification

    def __str__(self):
        return f"{self.username}"




class why_avenza(models.Model):

    
    description = models.CharField(max_length=500)  # Field for time slots


class cancelation_policy(models.Model):

    
    description = models.CharField(max_length=500)  # Field for time slots


class testimonials(models.Model):

    
    name = models.CharField(max_length=100)  # Field for time slots
    description = models.CharField(max_length=500)  # Field for time slots

