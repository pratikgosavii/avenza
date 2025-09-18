from django.db import models
from django.contrib.auth.models import AbstractUser
from admins.models import User
from location.models import Location
from category.models import *
# from orders.models import Order


class Vendor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="vendor")
    vendorname = models.CharField(max_length=255, null=True)
    vendorPhoneNumber = models.CharField(max_length=15)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="vendorLocation")
    is_approved = models.BooleanField(default=False)
    is_pending = models.BooleanField(default=True)
    category = models.ManyToManyField(Category)
    image = models.ImageField(upload_to='vendor_images/', null=True, blank=True)  # New image field
    portfolio_link = models.URLField(max_length=255, blank=True, null=True)  # New field for portfolio link
    is_available = models.BooleanField(default=True)  # New field to toggle availability

    def __str__(self):
        return self.vendorname or f"Vendor {self.id}"


class OrderCompletionImage(models.Model):
    vendor = models.ForeignKey(
        Vendor, 
        on_delete=models.CASCADE, 
        related_name='vendor_completion_images'  # Use a unique related name
    )
    completion_images = models.ImageField(upload_to='vendor_order_completion/')

    



class VendorAvailability(models.Model):
    vendor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='availability')
    date = models.DateField()

# class Review(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='reviews')
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="vendor")
#     rating = models.PositiveIntegerField(default=0)  # Assuming rating is from 0 to 5
#     comment = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f'Review by {self.user.username} on {self.package.title}'