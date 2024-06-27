from django.urls import path, include
from rest_framework import routers

from .views import HotelViewSet

router = routers.DefaultRouter()
router.register('hotels', HotelViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
]
