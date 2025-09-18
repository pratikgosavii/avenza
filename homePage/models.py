from django.db import models
from packages.models import Package
from category.models import Category
from location.models import Location
from subCategory.models import SubCategory


class HomeBanner(models.Model):
    title = models.CharField(max_length=225, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='homeBanners/')
    is_active = models.BooleanField(default=False)
    location = models.ManyToManyField(Location, related_name='homeBannerLocation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class HomeSection(models.Model):
    title = models.CharField(max_length=225, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='homeSections/', blank=True, null=True)
    is_active = models.BooleanField(default=False)
    categories = models.ManyToManyField(Category, related_name='sectionCategory')
    packages = models.ManyToManyField(Package, related_name='sectionPackage')
    location = models.ManyToManyField(Location, related_name='homeSectionLocation')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
