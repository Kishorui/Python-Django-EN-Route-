# from django.db import models
# from django.contrib.auth.models import User

# class Gallery(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='galleries')
#     name = models.CharField(max_length=255)
#     website = models.URLField(blank=True, null=True)
#     address = models.CharField(max_length=255, null=True, blank=True)
#     area = models.CharField(max_length=100, blank=True, null=True)
#     state = models.CharField(max_length=100, blank=True, null=True)  # ✅ Only one
#     postcode = models.CharField(max_length=20, blank=True, null=True)
#     contact_number = models.CharField(max_length=100, blank=True, null=True)
#     opening_hours = models.CharField(max_length=100, blank=True, null=True)
#     days_closed = models.CharField(max_length=255, blank=True, null=True)
#     gallery_image =models.ImageField(upload_to='gallery_images/', blank=True, null=True)
#     date =models.CharField(max_length=100, blank=True, null=True)
#     start_date = models.DateField(blank=True, null=True)
#     end_date = models.DateField(blank=True, null=True)
#     overview = models.TextField(blank=True, null=True)
#     lat= models.FloatField(blank=True, null=True)
#     long= models.FloatField(blank=True, null=True)

#     def __str__(self):
#         return self.name


# class Exhibition(models.Model):
#     gallery = models.ForeignKey(Gallery, related_name='exhibitions', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     artist = models.CharField(max_length=255)
#     start_date = models.DateField()
#     end_date = models.DateField()
#     description = models.TextField()
#     image = models.ImageField(upload_to='exhibition_images/', blank=True, null=True)

#     def __str__(self):
#         return self.title

# class GalleryImage(models.Model):
#     gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
#     image = models.ImageField(upload_to='gallery_images/')


from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

class Gallery(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='galleries')
    # Core / existing
    name = models.CharField(max_length=255)  # Gallery Name
    website = models.URLField(blank=True, null=True)
    address = models.CharField(max_length=255, null=True, blank=True)
    area = models.CharField(max_length=100, blank=True, null=True)  # Gallery Area
    suburb = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=20, blank=True, null=True)
    contact_number = models.CharField(max_length=100, blank=True, null=True)
    opening_hours_full = models.CharField(max_length=255, blank=True, null=True)  # Opening Hours in full
    opening_hours_breakdown = models.TextField(blank=True, null=True)        # Opening Hours (broken down by day in menu)
    days_closed = models.CharField(max_length=255, blank=True, null=True)
    closed_for_holidays = models.CharField(max_length=255, blank=True, null=True)
    overview = models.TextField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    # Map/coords
    lat = models.FloatField(blank=True, null=True)
    long = models.FloatField(blank=True, null=True)
    # Social
    instagram = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    # Art for sale (single record from Excel row)
    art_image = models.ImageField(upload_to='art_images/', blank=True, null=True)
    art_artist = models.CharField(max_length=255, blank=True, null=True)
    art_title = models.CharField(max_length=255, blank=True, null=True)
    art_price = models.CharField(max_length=100, blank=True, null=True)
    # Admin/billing/meta from Excel
    serial_no = models.CharField(max_length=50, blank=True, null=True)   # S No. (As per Map)
    paid_until = models.DateField(blank=True, null=True)  # For admin-only calendar dropdown
    gallery_active = models.BooleanField(default=True)    # For admin-only y/n
    password_login = models.CharField(max_length=255, blank=True, null=True)
    email_signin = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    def save(self, *args, user=None, **kwargs):
        # Restrict paid_until and gallery_active modifications to admins
        if self.pk:  # If updating an existing instance
            original = Gallery.objects.get(pk=self.pk)
            if user and not user.is_superuser:
                if self.paid_until != original.paid_until or self.gallery_active != original.gallery_active:
                    raise PermissionDenied("Only admins can modify paid_until or gallery_active fields.")
        super().save(*args, **kwargs)

class Artist(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip()

class Exhibition(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='exhibitions', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    artists = models.ManyToManyField(Artist, related_name='exhibitions')
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField()
    
    def __str__(self):
        return self.title

class GalleryImage(models.Model):
    gallery = models.ForeignKey(Gallery, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='gallery_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption for images

    def __str__(self):
        return f"Image for {self.gallery.name}"

class ExhibitionImage(models.Model):
    exhibition = models.ForeignKey(Exhibition, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='exhibition_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)  # Optional caption for images

    def __str__(self):
        return f"Image for {self.exhibition.title}"