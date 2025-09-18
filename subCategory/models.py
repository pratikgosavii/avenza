from django.db import models
from location.models import Location
from category.models import Category


class SubCategory(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='subCategories/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='subCategoryLocation')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='subCategory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
