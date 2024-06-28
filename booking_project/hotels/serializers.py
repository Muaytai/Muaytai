from rest_framework import serializers

from .models import Hotel


class HotelSerializer(serializers.ModelSerializer):
    photo = serializers.ImageField(read_only=True)

    class Meta:
        model = Hotel
        fields = ['id', 'name', 'description', 'location', 'price_per_night', 'rating', 'photo', 'created_at']
