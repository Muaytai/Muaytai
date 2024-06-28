from django.contrib import admin

from .models import Hotel


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    fields = ('name', 'description', 'location', 'price_per_night', 'rating', 'photo')
