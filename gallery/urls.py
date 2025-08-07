from django.urls import path
from .views import RegisterGalleryView, MyGalleryAPIView, GalleryListAPIView, GalleryDetailAPIView,GalleryMapAPIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('auth/register/', RegisterGalleryView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='login'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/me/', MyGalleryAPIView.as_view(), name='my-gallery'),
    path('galleries/', GalleryListAPIView.as_view(), name='gallery-list'),
    path('galleries/<int:pk>/', GalleryDetailAPIView.as_view(), name='gallery-detail'),
    path("galleries/map/", GalleryMapAPIView.as_view(), name="gallery-map"),
    
]
