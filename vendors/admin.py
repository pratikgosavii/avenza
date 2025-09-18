from django.contrib import admin

from .models import *



admin.site.register(Vendor)
admin.site.register(VendorAvailability)
admin.site.register(OrderCompletionImage)

