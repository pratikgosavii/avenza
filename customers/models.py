from django.db import models
from admins.models import User
from location.models import Location


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="customer")
    customerPhoneNumber = models.CharField(max_length=15, null=True, blank=True)
    dateOfBirth = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=255, null=True, blank=True)
    address1 = models.CharField(max_length=255, null=True, blank=True)
    address2 = models.CharField(max_length=255, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name="customerLocation", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)



class Ticket(models.Model):
    STATUS_CHOICES = [
        ("open", "Open"),
        ("in_progress", "In Progress"),
        ("resolved", "Resolved"),
        ("closed", "Closed"),
    ]

    order = models.ForeignKey('orders.Order', on_delete=models.CASCADE, related_name='tickets')  # Link to the Order model
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Link to the Customer model
    vendor = models.ForeignKey(User, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL here
    issue_description = models.TextField()  # Field for describing the issue
    image = models.ImageField(upload_to='ticket/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="open")  # Status of the ticket
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the ticket was created
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp when the ticket was last updated

    def __str__(self):
        return f'Ticket {self.id} - {self.status} - {self.order.id}'