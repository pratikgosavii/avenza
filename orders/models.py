from django.db import models
from vendors.models import *
from customers.models import *
from packages.models import *

# Create your models here.



class Order(models.Model):

    date = models.DateField()  # Field for selecting the date
    SLOT_CHOICES = [
        ("1-2", "1 PM - 2 PM"),
        ("2-3", "2 PM - 3 PM"),
        ("3:00 PM - 6:00 PM", "3:00 PM - 6:00 PM"),    # add more here
    ]
    STATUS_CHOICES = [
        ("new_order", "New Order"),
        ("ongoing", "Ongoing"),
        ("completed", "Completed"),    # add more here
        ("accepted", "Accepted"),    # add more here
        ("rejected", "Rejected"),    # add more here
        ("declined", "Declined"),    # add more here
    ]

    PAYMENT_MODE_CHOICES = [
        ("1-2", "1 PM - 2 PM"),
        ("2-3", "2 PM - 3 PM"),
        ("3:00 PM - 6:00 PM", "3:00 PM - 6:00 PM"),    # add more here
    ]
    slot = models.CharField(max_length=20, choices=SLOT_CHOICES)  # Field for time slots
    payment_mode = models.CharField(max_length=20, choices=PAYMENT_MODE_CHOICES, null=True, blank=True)  # Field for time slots
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="new_order")  # Field for time slots

    
    packageId = models.ForeignKey(Package, on_delete=models.CASCADE)
    locationId = models.ForeignKey(Location, on_delete=models.CASCADE)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE, null=True, blank=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shipping_address = models.CharField(max_length=120, unique=False)
    pincode = models.CharField(max_length=120, unique=False)
    city = models.CharField(max_length=120, unique=False)
    contact_no  = models.BigIntegerField()
    total_amount  = models.IntegerField()
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now=True)


class OrderCustomization(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="customizations"
    )
    customization = models.ForeignKey(Customization, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    