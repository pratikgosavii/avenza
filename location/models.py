from django.db import models


class Location(models.Model):
    title = models.CharField(max_length=225)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='location/', null=True, blank=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
