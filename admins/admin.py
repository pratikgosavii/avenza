from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
# Register the User model

from .models import *
admin.site.register(User, UserAdmin)
admin.site.register(why_avenza)