from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views


auth_urls = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]

urlpatterns = [
    # Отели
    path('hotels/', views.HotelListView.as_view(), name='hotel-list'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel-detail'),

    # Бронирования
    path('bookings/', views.BookingListCreateView.as_view(), name='booking-list'),  # Создание бронирования
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),
    # Просмотр, редактирование, удаление бронирования

    # Регистрация и просмотр пользователей
    path('register/', views.UserCreateView.as_view(), name='user-create'),  # Создание пользователя
    path('users/', views.UserList.as_view(), name='user-list'),  # Получение списка пользователей

    # Аутентификация
    path('auth/', include(auth_urls)),  # Используйте include для auth_urls

]