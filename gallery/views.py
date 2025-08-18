# import re 
# from datetime import datetime, timedelta
# from django.db.models import F, Value
# from django.db.models.functions import Replace
# from rest_framework import generics, permissions, filters as drf_filters
# from django_filters import rest_framework as filters
# from django.shortcuts import get_object_or_404

# from .models import Gallery
# from .serializers import RegisterGallerySerializer, GallerySerializer,GalleryMapSerializer
# from .utils import get_days_in_range, gallery_is_open_for_range  # ✅ now from utils.py



# # ==============================
# # Registration View
# # ==============================
# class RegisterGalleryView(generics.CreateAPIView):
#     queryset = Gallery.objects.all()
#     serializer_class = RegisterGallerySerializer
#     permission_classes = [permissions.AllowAny]


# # ==============================
# # My Gallery Profile View
# # ==============================
# class MyGalleryAPIView(generics.RetrieveUpdateAPIView):
#     serializer_class = GallerySerializer
#     permission_classes = [permissions.IsAuthenticated]

#     def get_object(self):
#         return get_object_or_404(Gallery, user=self.request.user)


# # ==============================
# # Gallery List View
# # ==============================

# class GalleryListAPIView(generics.ListAPIView):
#     serializer_class = GallerySerializer
#     permission_classes = []

#     def normalize_text(self, text):
#         """Remove spaces, slashes, commas, dots, dashes, lowercase."""
#         if not text:
#             return ""
#         return re.sub(r"[\s/,\.\-]+", "", text).lower()

#     def get_queryset(self):
#         qs = Gallery.objects.all()

#         # ✅ Starts_with filter (ignore spaces & punctuation)
#         starts_with = self.request.query_params.get('starts_with')
#         if starts_with:
#             clean_starts = self.normalize_text(starts_with)
#             qs = [g for g in qs if self.normalize_text(g.name).startswith(clean_starts)]

#         # ✅ Area filter (ignore spaces & punctuation,allow 'all')
#         area = self.request.query_params.get('area')
#         if area and self.normalize_text(area) != "all":
#             clean_area = self.normalize_text(area)
#             qs = [g for g in qs if self.normalize_text(g.area) == clean_area]

#         # ✅ Name filter (ignore spaces & punctuation)
#         name = self.request.query_params.get('name')
#         if name:
#             clean_name = self.normalize_text(name)
#             qs = [g for g in qs if self.normalize_text(g.name) == clean_name]

#         return qs
# # ==============================
# # Gallery Detail View
# # ==============================
# class GalleryDetailAPIView(generics.RetrieveAPIView):
#     queryset = Gallery.objects.all()
#     serializer_class = GallerySerializer
#     permission_classes = []  # public

#     def get_serializer_context(self):
#         """Pass date range to serializer so detail view can calculate status."""
#         context = super().get_serializer_context()
#         context["open_from"] = self.request.query_params.get('open_from')
#         context["open_until"] = self.request.query_params.get('open_until')
#         return context
    

# class GalleryMapAPIView(generics.ListAPIView):
#     """
#     API endpoint to list galleries for map display.
#     Supports filtering by:
#       - area (case-insensitive exact match)
#       - id (exact match)
#       - name (case-insensitive partial match)
#     """
#     serializer_class = GalleryMapSerializer
#     permission_classes = []  # public

#     def get_queryset(self):
#         # Start with galleries that have lat/long
#         qs = Gallery.objects.exclude(lat__isnull=True).exclude(long__isnull=True)

#         # Filter by id if provided
#         gallery_id = self.request.query_params.get("id")
#         if gallery_id:
#             try:
#                 qs = qs.filter(id=int(gallery_id))
#             except ValueError:
#                 pass  # ignore invalid id

#         # Filter by area if provided
#         area = self.request.query_params.get("area")
#         if area:
#             qs = qs.filter(area__iexact=area)

#         # Filter by name if provided
#         name = self.request.query_params.get("name")
#         if name:
#             qs = qs.filter(name__icontains=name)

#         return qs

import re 
from datetime import datetime, timedelta
from django.db.models import F, Value
from django.db.models.functions import Replace
from rest_framework import generics, permissions, filters as drf_filters
from django_filters import rest_framework as filters
from django.shortcuts import get_object_or_404

from .models import Gallery
from .serializers import RegisterGallerySerializer, GallerySerializer, GalleryMapSerializer
from .utils import get_days_in_range, gallery_is_open_for_range  # ✅ now from utils.py

# ==============================
# Registration View
# ==============================
class RegisterGalleryView(generics.CreateAPIView):
    queryset = Gallery.objects.all()
    serializer_class = RegisterGallerySerializer
    permission_classes = [permissions.AllowAny]

# ==============================
# My Gallery Profile View
# ==============================
class MyGalleryAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = GallerySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return get_object_or_404(Gallery, user=self.request.user)

# ==============================
# Gallery List View
# ==============================
class GalleryListAPIView(generics.ListAPIView):
    serializer_class = GallerySerializer
    permission_classes = []

    def normalize_text(self, text):
        """Remove spaces, slashes, commas, dots, dashes, lowercase."""
        if not text:
            return ""
        return re.sub(r"[\s/,\.\-]+", "", text).lower()

    def get_queryset(self):
        qs = Gallery.objects.all()

        # ✅ Starts_with filter (ignore spaces & punctuation)
        starts_with = self.request.query_params.get('starts_with')
        if starts_with:
            clean_starts = self.normalize_text(starts_with)
            qs = [g for g in qs if self.normalize_text(g.name).startswith(clean_starts)]

        # ✅ Area filter (ignore spaces & punctuation,allow 'all')
        area = self.request.query_params.get('area')
        if area and self.normalize_text(area) != "all":
            clean_area = self.normalize_text(area)
            qs = [g for g in qs if self.normalize_text(g.area) == clean_area]

        # ✅ Name filter (ignore spaces & punctuation)
        name = self.request.query_params.get('name')
        if name:
            clean_name = self.normalize_text(name)
            qs = [g for g in qs if self.normalize_text(g.name) == clean_name]

        return qs

# ==============================
# Gallery Detail View
# ==============================
class GalleryDetailAPIView(generics.RetrieveAPIView):
    queryset = Gallery.objects.all()
    serializer_class = GallerySerializer
    permission_classes = []  # public

    def get_serializer_context(self):
        """Pass date range to serializer so detail view can calculate status."""
        context = super().get_serializer_context()
        context["open_from"] = self.request.query_params.get('open_from')
        context["open_until"] = self.request.query_params.get('open_until')
        return context

class GalleryMapAPIView(generics.ListAPIView):
    """
    API endpoint to list galleries for map display.
    Supports filtering by:
      - area (case-insensitive exact match)
      - id (exact match)
      - name (case-insensitive partial match)
    """
    serializer_class = GalleryMapSerializer
    permission_classes = []  # public

    def get_queryset(self):
        # Start with galleries that have lat/long
        qs = Gallery.objects.exclude(lat__isnull=True).exclude(long__isnull=True)

        # Filter by id if provided
        gallery_id = self.request.query_params.get("id")
        if gallery_id:
            try:
                qs = qs.filter(id=int(gallery_id))
            except ValueError:
                pass  # ignore invalid id

        # Filter by area if provided
        area = self.request.query_params.get("area")
        if area:
            qs = qs.filter(area__iexact=area)

        # Filter by name if provided
        name = self.request.query_params.get("name")
        if name:
            qs = qs.filter(name__icontains=name)

        return qs