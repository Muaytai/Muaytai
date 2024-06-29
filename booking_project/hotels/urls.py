from django.urls import path
from . import views

urlpatterns = [
    # Отели
    path('hotels/', views.HotelListCreateView.as_view(), name='hotel-list-create'),
    path('hotels/<int:pk>/', views.HotelDetailView.as_view(), name='hotel-detail'),

    # Бронирования
    path('bookings/', views.BookingListCreateView.as_view(), name='booking-list-create'),
    path('bookings/<int:pk>/', views.BookingDetailView.as_view(), name='booking-detail'),

    # Регистрация
    path('register/', views.UserCreateView.as_view(), name='user-create'),
]