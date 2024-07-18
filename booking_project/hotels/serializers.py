from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Hotel, Booking, Profile


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,  # Пароль не будет возвращаться в ответе
                'required': True
            }
        }

    def create(self, validated_data):
        username = validated_data['username'],
        email = validated_data['email'],
        password = validated_data['password']


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'


class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'
        read_only_fields = ['user']  # Пользователь будет автоматически добавляться при бронировании


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['full_name', 'birth_date', 'address', 'phone_number', 'user']
        read_only_fields = ['user']

    def validate(self, data):
        if 'birth_date' not in data or not data['birth_date']:
            raise serializers.ValidationError({'birth_date': 'Дата рождения обязательна.'})
        return data
