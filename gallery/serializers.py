# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Gallery, Exhibition, GalleryImage
# from datetime import datetime
# from .utils import get_days_in_range, gallery_is_open_for_range  # ✅ from utils.py

# class RegisterGallerySerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username')
#     password = serializers.CharField(write_only=True, source='user.password')

#     class Meta:
#         model = Gallery
#         fields = [
#             'username', 'password', 'name', 'website', 'address', 'contact_number',
#             'opening_hours', 'area', 'date'
#         ]

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = User.objects.create_user(
#             username=user_data['username'],
#             password=user_data['password']
#         )
#         return Gallery.objects.create(user=user, **validated_data)
# class ExhibitionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Exhibition
#         fields = ['title', 'artist', 'start_date', 'end_date', 'description', 'image']

# class GalleryImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GalleryImage
#         fields = ['id', 'image']


# class GallerySerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='user.email', read_only=True)
#     images = GalleryImageSerializer(many=True, read_only=True)
#     exhibitions = ExhibitionSerializer(many=True, read_only=True)
#     status = serializers.SerializerMethodField()  # ✅ dynamic open/closed

#     class Meta:
#         model = Gallery
#         fields = [
#             'id', 'name', 'email', 'address', 'contact_number', 'area',
#             'start_date', 'end_date', 'overview', 'days_closed',
#             'images', 'exhibitions', 'status'
#         ]

#     def get_status(self, obj):
#         """Check closed status based on today's day OR ?date=YYYY-MM-DD"""
#         request = self.context.get('request')
#         check_day = None

#         # ✅ Check if ?date=YYYY-MM-DD is in query params
#         if request:
#             date_str = request.query_params.get('date')
#             if date_str:
#                 try:
#                     check_day = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
#                 except ValueError:
#                     pass  # If invalid date, fallback to today

#         # ✅ If no valid date provided, use today's day
#         if not check_day:
#             check_day = datetime.today().strftime("%A")

#         # ✅ Compare with days_closed field
#         if obj.days_closed:
#             closed_days = [d.strip().lower() for d in obj.days_closed.split(',')]
#             if check_day.lower() in closed_days:
#                 return "closed"

#         return "open"
    
# class GalleryMapSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Gallery
#         fields = ["id", "name", "lat", "long", "area"]


# from rest_framework import serializers
# from django.contrib.auth.models import User
# from .models import Gallery, Exhibition, GalleryImage
# from datetime import datetime
# from .utils import get_days_in_range, gallery_is_open_for_range

# class RegisterGallerySerializer(serializers.ModelSerializer):
#     username = serializers.CharField(source='user.username')
#     password = serializers.CharField(write_only=True, source='user.password')

#     class Meta:
#         model = Gallery
#         fields = [
#             'username', 'password', 'name', 'website', 'address', 'contact_number',
#             'opening_hours_full', 'area', 'date'
#         ]

#     def create(self, validated_data):
#         user_data = validated_data.pop('user')
#         user = User.objects.create_user(
#             username=user_data['username'],
#             password=user_data['password']
#         )
#         return Gallery.objects.create(user=user, **validated_data)

# class ExhibitionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Exhibition
#         fields = ['title', 'artist', 'start_date', 'end_date', 'description', 'image']

# class GalleryImageSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = GalleryImage
#         fields = ['id', 'image']

# class GallerySerializer(serializers.ModelSerializer):
#     email = serializers.EmailField(source='user.email', read_only=True)
#     images = GalleryImageSerializer(many=True, read_only=True)
#     exhibitions = ExhibitionSerializer(many=True, read_only=True)
#     status = serializers.SerializerMethodField()

#     class Meta:
#         model = Gallery
#         fields = [
#             'id', 'name', 'email', 'address', 'contact_number', 'area',
#             'start_date', 'end_date', 'overview', 'days_closed',
#             'images', 'exhibitions', 'status',
#             'suburb', 'opening_hours_full', 'opening_hours_breakdown', 'closed_for_holidays',
#             'instagram', 'facebook', 'art_artist', 'art_title', 'art_price', 'serial_no',
#             'paid_until', 'gallery_active', 'password_login', 'email_signin'
#         ]

#     def get_status(self, obj):
#         """Check closed status based on today's day OR ?date=YYYY-MM-DD"""
#         request = self.context.get('request')
#         check_day = None

#         if request:
#             date_str = request.query_params.get('date')
#             if date_str:
#                 try:
#                     check_day = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
#                 except ValueError:
#                     pass

#         if not check_day:
#             check_day = datetime.today().strftime("%A")

#         if obj.days_closed:
#             closed_days = [d.strip().lower() for d in obj.days_closed.split(',')]
#             if check_day.lower() in closed_days:
#                 return "closed"

#         return "open"

# class GalleryMapSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Gallery
#         fields = ["id", "name", "lat", "long", "area"]


from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Gallery, Exhibition, GalleryImage, Artist, ExhibitionImage
from datetime import datetime
import re
from .utils import get_days_in_range, gallery_is_open_for_range

class RegisterGallerySerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    password = serializers.CharField(write_only=True, source='user.password')

    class Meta:
        model = Gallery
        fields = [
            'username', 'password', 'name', 'website', 'address', 'contact_number',
            'opening_hours_full', 'area', 'start_date', 'end_date'  # Updated 'date' to 'start_date'/'end_date'
        ]

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        user = User.objects.create_user(
            username=user_data['username'],
            password=user_data['password']
        )
        return Gallery.objects.create(user=user, **validated_data)

class ExhibitionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExhibitionImage
        fields = ['id', 'image', 'caption']

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id', 'first_name', 'last_name']

class GalleryImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GalleryImage
        fields = ['id', 'image', 'caption']  # Added 'caption' field

class ExhibitionSerializer(serializers.ModelSerializer):
    artists = ArtistSerializer(many=True, read_only=True)
    images = ExhibitionImageSerializer(many=True, read_only=True)  # Nested serializer for images

    class Meta:
        model = Exhibition
        fields = ['id', 'title', 'gallery', 'artists', 'start_date', 'end_date', 'description', 'images']

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        print(f"Serializing Exhibition {instance.title} (ID: {instance.id}): Artists = {[str(a) for a in instance.artists.all()]}")
        if ret['start_date']:
            ret['start_date'] = datetime.strptime(ret['start_date'], '%Y-%m-%d').strftime('%B %d, %Y')
        if ret['end_date']:
            ret['end_date'] = datetime.strptime(ret['end_date'], '%Y-%m-%d').strftime('%B %d, %Y')
        return ret

class GallerySerializer(serializers.ModelSerializer):
    email = serializers.CharField(source='email_signin', read_only=True)
    images = GalleryImageSerializer(many=True, read_only=True)
    exhibitions = ExhibitionSerializer(many=True, read_only=True)
    status = serializers.SerializerMethodField()
    paid_until = serializers.DateField(read_only=True)
    gallery_active = serializers.BooleanField(read_only=True)

    class Meta:
        model = Gallery
        fields = [
            'id', 'name', 'email', 'website', 'address', 'contact_number', 'area',
            'overview', 'days_closed', 'images', 'exhibitions', 'status',
            'suburb', 'opening_hours_full', 'opening_hours_breakdown', 'closed_for_holidays',
            'instagram', 'facebook', 'art_image', 'art_artist', 'art_title', 'art_price',
            'serial_no', 'paid_until', 'gallery_active', 'password_login', 'lat', 'long'
        ]

    def to_representation(self, instance):
        ret = super().to_representation(instance)
       # print(f"Serialized {instance.name}: email={ret['email']}, paid_until={ret['paid_until']}, gallery_active={ret['gallery_active']}")
        return ret

    def get_status(self, obj):
        request = self.context.get('request')
        open_from = self.context.get('open_from')
        open_until = self.context.get('open_until')

        if open_from and open_until:
            try:
                start_date = datetime.strptime(open_from, '%Y-%m-%d').date()
                end_date = datetime.strptime(open_until, '%Y-%m-%d').date()
                days = get_days_in_range(start_date, end_date)
                return gallery_is_open_for_range(obj, days)
            except ValueError:
                pass

        check_day = None
        if request:
            date_str = request.query_params.get('date')
            if date_str:
                try:
                    check_day = datetime.strptime(date_str, "%Y-%m-%d").strftime("%A")
                except ValueError:
                    pass
        if not check_day:
            check_day = datetime.today().strftime("%A")
        if obj.days_closed:
            closed_days = [d.strip().lower() for d in obj.days_closed.split(',')]
            if check_day.lower() in closed_days:
                return "closed"
        return "open"

class GalleryMapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gallery
        fields = ["id", "name", "lat", "long", "area"]