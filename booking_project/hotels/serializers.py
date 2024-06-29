from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Hotel, Booking


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']  # Выбор полей для сериализации
        extra_kwargs = {'password': {'write_only': True}}  # Пароль не будет возвращаться в ответе

    def create(self, validated_data):  # Хеширование пароля при создании пользователя
        user = User.objects.create_user(**validated_data)
        return user


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'  # Сериализация всех полей модели


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user']  # Пользователь будет автоматически добавляться при бронировании
