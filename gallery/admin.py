# from django.contrib import admin
# from .models import Gallery, Exhibition, GalleryImage

# class ExhibitionAdmin(admin.ModelAdmin):
#     list_display = ['gallery','title', 'artist', 'start_date', 'end_date']
#     list_filter = ['gallery', 'start_date']
#     search_fields = ['title', 'artist', 'gallery__name']
#     autocomplete_fields = ['gallery']  # improves usability when many galleries exist

# class GalleryImageInline(admin.TabularInline):
#     model = GalleryImage
#     extra = 1

# class GalleryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'area', 'address','website','days_closed','lat','long']
#     search_fields = ['name', 'area']
#     inlines = [GalleryImageInline]

# admin.site.register(Gallery, GalleryAdmin)
# admin.site.register(Exhibition, ExhibitionAdmin)

# from django.contrib import admin
# from .models import Gallery, Exhibition, GalleryImage

# class ExhibitionAdmin(admin.ModelAdmin):
#     list_display = ['gallery','title', 'artist', 'start_date', 'end_date']
#     list_filter = ['gallery', 'start_date']
#     search_fields = ['title', 'artist', 'gallery__name']
#     autocomplete_fields = ['gallery']  # improves usability when many galleries exist

# class GalleryImageInline(admin.TabularInline):
#     model = GalleryImage
#     extra = 1

# class GalleryAdmin(admin.ModelAdmin):
#     list_display = ['name', 'area', 'suburb', 'address', 'website', 'days_closed', 'opening_hours_full', 'lat', 'long']  # Added new fields
#     search_fields = ['name', 'area', 'suburb']  # Added suburb
#     inlines = [GalleryImageInline]

# admin.site.register(Gallery, GalleryAdmin)
# admin.site.register(Exhibition, ExhibitionAdmin)

from django.contrib import admin
from .models import Gallery, Exhibition, Artist, GalleryImage, ExhibitionImage

# Inline for GalleryImage
class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1  # Number of empty forms to display
    fields = ['image', 'caption']  # Include image and caption fields

# Inline for ExhibitionImage
class ExhibitionImageInline(admin.TabularInline):
    model = ExhibitionImage
    extra = 1  # Number of empty forms to display
    fields = ['image', 'caption']  # Include image and caption fields

@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    inlines = [GalleryImageInline]  # Add inline for multiple images
    list_display = ['name', 'email_signin', 'website', 'paid_until', 'gallery_active']
    list_filter = ['gallery_active', 'area', 'state']
    search_fields = ['name', 'email_signin', 'suburb']
    fieldsets = (
        (None, {
            'fields': ('user', 'name', 'email_signin', 'password_login')
        }),
        ('Contact Info', {
            'fields': ('website', 'address', 'area', 'suburb', 'state', 'postcode', 'contact_number')
        }),
        ('Operation Details', {
            'fields': ('opening_hours_full', 'opening_hours_breakdown', 'days_closed', 'closed_for_holidays')
        }),
        ('Additional Info', {
            'fields': ('overview', 'instagram', 'facebook', 'art_image', 'art_artist', 'art_title', 'art_price')
        }),
        ('Admin Fields', {
            'fields': ('serial_no', 'paid_until', 'gallery_active'),
            'classes': ('collapse',),  # Collapse admin fields by default
        }),
        ('Location', {
            'fields': ('lat', 'long')
        }),
    )

    def save_model(self, request, obj, form, change):
        # Attach the current user to the save operation for permission checking
        obj.save(user=request.user)

    def get_readonly_fields(self, request, obj=None):
        # Restrict non-superusers from editing paid_until and gallery_active
        if not request.user.is_superuser:
            return ['paid_until', 'gallery_active']
        return []

@admin.register(Exhibition)
class ExhibitionAdmin(admin.ModelAdmin):
    inlines = [ExhibitionImageInline]  # Add inline for multiple images
    list_display = ['title', 'gallery', 'start_date', 'end_date']
    list_filter = ['gallery', 'start_date']
    search_fields = ['title', 'gallery__name']
    autocomplete_fields = ['gallery']
    fields = ['gallery', 'title', 'artists', 'start_date', 'end_date', 'description']

@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name']
    search_fields = ['first_name', 'last_name']

@admin.register(GalleryImage)
class GalleryImageAdmin(admin.ModelAdmin):
    list_display = ['gallery', 'image', 'caption']
    search_fields = ['gallery__name', 'caption']

@admin.register(ExhibitionImage)
class ExhibitionImageAdmin(admin.ModelAdmin):
    list_display = ['exhibition', 'image', 'caption']
    search_fields = ['exhibition__title', 'caption']