from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    location = models.CharField(max_length=200)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    rating = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    photo = models.ImageField(upload_to='hotel_photos', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add=True

    def __str__(self):
        return f"{self.name} - {self.description} | {self.price_per_night}BYN | {self.rating}"


class Booking(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name='bookings')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    check_in = models.DateField()
    check_out = models.DateField()
    guests = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking {self.id}: {self.user} - {self.hotel.name}"

    def get_total_price(self):
        nights = (self.check_out - self.check_in).days
        total_price = nights * self.hotel.price_per_night
        return total_price

    def clean(self):
        if self.check_out <= self.check_in:
            self.add_error('check_out', 'Check-out date must be after check-in date.')
        return super().clean()
