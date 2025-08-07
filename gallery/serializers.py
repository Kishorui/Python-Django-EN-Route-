from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Gallery, Exhibition, GalleryImage
from datetime import datetime
from .utils import get_days_in_range, gallery_is_open_for_range  # ✅ from utils.py

class RegisterGallerySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(write_only=True, source='user.password')

    class Meta:
        model = Gallery
        fields = [
            'username', 'password', 'name', 'website', 'address', 'contact_number',
            'opening_hours', 'area', 'date'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password']
        )
        return Gallery.objects.create(user=user, **validated_data)
class ExhibitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exhibition
        fields = ['title', 'artist', 'start_date', 'end_date', 'description', 'image']

class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image']


class GallerySerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source='user.email', read_only=True)
    images = GalleryImageSerializer(many=True, read_only=True)
    exhibitions = ExhibitionSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()  # ✅ dynamic open/closed

    class Meta:
        model = Gallery
        fields = [
            'id', 'name', 'email', 'address', 'contact_number', 'area',
            'start_date', 'end_date', 'overview', 'days_closed',
            'images', 'exhibitions', 'status'
        ]

    def get_status(self, obj):
        """Check closed status based on today's day OR ?date=YYYY-MM-DD"""
        request = self.context.get('request')
        check_day = None

        # ✅ Check if ?date=YYYY-MM-DD is in query params
        if request:
            date_str = request.query_params.get('date')
            if date_str:
                try:
                    check_day = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
                except ValueError:
                    pass  # If invalid date, fallback to today

        # ✅ If no valid date provided, use today's day
        if not check_day:
            check_day = datetime.today().strftime("%A")

        # ✅ Compare with days_closed field
        if obj.days_closed:
            closed_days = [d.strip().lower() for d in obj.days_closed.split(',')]
            if check_day.lower() in closed_days:
                return "closed"

        return "open"
    
class GalleryMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["id", "name", "lat", "long", "area"]