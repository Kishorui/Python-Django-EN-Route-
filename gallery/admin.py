from django.contrib import admin
from .models import Gallery, Exhibition, GalleryImage

class ExhibitionAdmin(admin.ModelAdmin):
    list_display = ['gallery','title', 'artist', 'start_date', 'end_date']
    list_filter = ['gallery', 'start_date']
    search_fields = ['title', 'artist', 'gallery__name']
    autocomplete_fields = ['gallery']  # improves usability when many galleries exist

class GalleryImageInline(admin.TabularInline):
    model = GalleryImage
    extra = 1

class GalleryAdmin(admin.ModelAdmin):
    list_display = ['name', 'area', 'address','website','days_closed','lat','long']
    search_fields = ['name', 'area']
    inlines = [GalleryImageInline]

admin.site.register(Gallery, GalleryAdmin)
admin.site.register(Exhibition, ExhibitionAdmin)
