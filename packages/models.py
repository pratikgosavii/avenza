from django.db import models
from location.models import Location  # Import Location model
from category.models import Category  # Import Category model
from subCategory.models import SubCategory  # Import SubCategory model (if you plan to use it)


# Customization Model
class Customization(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='customizations/')
    description = models.TextField()


# PackageLocationPrice Model (For price association with category and location)
class PackageInclusion(models.Model):
    
    title = models.CharField(max_length=255)

# PackageLocationPrice Model (For price association with category and location)
class need_to_know(models.Model):
    
    title = models.CharField(max_length=255)

   


# Package Model
class Package(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField()
    short_description = models.TextField()
    image = models.ImageField(upload_to='packages/')
    is_active = models.BooleanField(default=False)
    customizations = models.ManyToManyField(Customization, related_name='packageCustomizations')  # Link to Customization
    package_inclusion = models.ManyToManyField(PackageInclusion, related_name='packageInclusion')  # Link to Customization
    need_to_know = models.ManyToManyField(need_to_know, related_name='packageneed_to_know')  # Link to Customization
    categories = models.ManyToManyField(Category, related_name='packageCategories')  # Many-to-many with Category
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


# PackageLocationPrice Model (For price association with category and location)
class PackageLocationPrice(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE, related_name='package_location_prices')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='package_category')  # ForeignKey to Category
    location = models.ForeignKey(Location, on_delete=models.CASCADE)  # ForeignKey to Location
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.package.title} - {self.category.title} - {self.location.title} - ${self.price}'
    


