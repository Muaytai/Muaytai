from rest_framework import serializers
from .models import CustomUser, Hotel, Booking
from datetime import date


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'name', 'last_name', 'phone_number', 'address')


class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = ('id', 'name', 'description', 'city', 'country', 'price_per_night', 'currency', 'rating')


class BookingSerializer(serializers.ModelSerializer):
    user = CustomUserSerializer()
    hotel = HotelSerializer()

    class Meta:
        model = Booking
        fields = (
            'id', 'user', 'hotel', 'check_in_date', 'check_out_date', 'number_of_guests', 'room_type', 'total_price',
            'status')
        depth = 1

    def validate(self, data):
        check_in_date = data.get('check_in_date')
        check_out_date = data.get('check_out_date')

        if check_in_date < date.today():
            raise serializers.ValidationError("Дата заезда не может быть раньше текущей даты.")

        if check_out_date <= check_in_date:
            raise serializers.ValidationError("Дата выезда должна быть позже даты заезда.")

        return data

    def validate_number_of_guests(self, value):
        if value <= 0:
            raise serializers.ValidationError("Количество гостей должно быть больше 0.")
        return value
