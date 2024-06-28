from rest_framework import filters
from django_filters.rest_framework import DjangoFilterBackend


class HotelFilter(filters.OrderingFilter):
    fields = ['name', 'location', 'rating']
