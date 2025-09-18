from django.contrib import admin
from .models import *

from category.models import Category


admin.site.register(Package)
admin.site.register(Category)
admin.site.register(Customization)
admin.site.register(PackageLocationPrice)
admin.site.register(need_to_know)