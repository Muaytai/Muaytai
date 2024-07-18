from django.contrib import admin

from .models import Hotel, Booking, Profile  # Импорт модели Profile


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'location', 'price_per_night', 'rating', 'photo')
    list_display = ('name', 'location', 'price_per_night', 'rating')
    search_fields = ('name', 'location')
    ordering = ('name',)
    readonly_fields = ('created_at',)
    list_filter = ('rating',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'user', 'check_in', 'check_out', 'guests')
    list_filter = ('hotel', 'user', 'check_in', 'check_out')
    search_fields = ('hotel__name', 'user__username')
    readonly_fields = ('created_at',)


@admin.register(Profile)  # Регистрация модели Profile
class ProfileAdmin(admin.ModelAdmin):
    fields = ('user', 'full_name', 'birth_date', 'address', 'phone_number')
    list_display = ('user', 'full_name', 'birth_date', 'address', 'phone_number')
    search_fields = ('user__username', 'full_name')
    ordering = ('user',)
