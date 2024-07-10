from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views

auth_urls = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    # Отели
    path('hotels/', views.HotelListCreateView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel-detail'),

    # Бронирования
    path('bookings/', views.BookingListCreateView.as_view(), name='booking-list'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),

    # Регистрация и просмотр пользователей
    path('register/', views.UserCreateView.as_view(), name='user-create'),
    path('users/', views.UserList.as_view(), name='user-list'),

    # Аутентификация
    path('auth/', include(auth_urls)),
]