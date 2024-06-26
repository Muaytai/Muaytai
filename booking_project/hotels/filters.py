from rest_framework import filters


class HotelFilter(filters.OrderingFilter):
    fields = ['name', 'location', 'rating']
