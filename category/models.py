from django.db import models
from location.models import Location


class Category(models.Model):
    title = models.CharField(max_length=225)
    sub_title_category = models.CharField(max_length=225)
    description = models.TextField(null=True, blank=True)
    icon = models.ImageField(upload_to='categories/', null=True, blank=True)
    category_image = models.ImageField(upload_to='categories/', null=True, blank=True)
    location = models.ManyToManyField(Location, related_name='categories')
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class CategoryBannerImage(models.Model):
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='category_banner_images'  # Use a unique related name
    )
    image = models.ImageField(upload_to='categories/banner_images/')

    def __str__(self):
        return f"Image for {self.category.title}"

