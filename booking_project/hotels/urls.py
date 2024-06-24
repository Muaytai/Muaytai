from django.urls import path, include
from rest_framework import routers

from .views import HotelViewSet, CustomUserList, CustomUserDetail, BookingList, BookingDetail

router = routers.DefaultRouter()
router.register('hotels', HotelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('users/', CustomUserList.as_view(), name='user-list'),
    path('users/<int:pk>/', CustomUserDetail.as_view(), name='user-detail'),
    path('bookings/', BookingList.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', BookingDetail.as_view(), name='booking-detail'),
]
