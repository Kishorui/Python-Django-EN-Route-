from django.db import models
from django.contrib.auth.models import User

class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='galleries')
    name = models.CharField(max_length=255)
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)  # ✅ Only one
    postcode = models.CharField(max_length=20, blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    opening_hours = models.CharField(max_length=100, blank=True, null=True)
    days_closed = models.CharField(max_length=255, blank=True, null=True)
    gallery_image =models.ImageField(upload_to='gallery_images/', blank=True, null=True)
    date =models.CharField(max_length=100, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    lat= models.FloatField(blank=True, null=True)
    long= models.FloatField(blank=True, null=True)

    def __str__(self):
        return self.name


class Exhibition(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='exhibitions', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    artist = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField()
    image = models.ImageField(upload_to='exhibition_images/', blank=True, null=True)

    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_images/')
