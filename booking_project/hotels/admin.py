from django.contrib import admin

from .models import Hotel


class HotelAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', 'city', 'price_per_night', 'rating')
    search_fields = ('name', 'description', 'city', 'country')


admin.site.register(Hotel, HotelAdmin)
