from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date


class CustomUser(AbstractUser):
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, blank=True)
    phone_number = PhoneNumberField(blank=True)
    address = models.TextField(blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='custom_user_set',  # Уникальное имя для обратной ссылки
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='custom_user_set',  # Уникальное имя для обратной ссылки
    )


class Hotel(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    city = models.CharField(max_length=30)
    country = models.CharField(max_length=100)
    price_per_night = models.IntegerField(validators=[MinValueValidator(0)])
    currency = models.CharField(max_length=3, default='BYN')
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[
        MinValueValidator(0.0),
        MaxValueValidator(5.0)
    ])

    def __str__(self):
        return f"{self.name} ({self.city}, {self.country}) | {self.price_per_night} {self.currency} | {self.rating}"


class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    number_of_guests = models.IntegerField(validators=[MinValueValidator(1)])
    room_type = models.CharField(max_length=50, blank=True)
    total_price = models.IntegerField(blank=True)
    status = models.CharField(max_length=20, choices=(
        ('Pending', 'Pending'),
        ('Confirmed', 'Confirmed'),
        ('Cancelled', 'Cancelled'),
    ), default='Pending')

    def __str__(self):
        return f"{self.user.username} - {self.hotel.name} ({self.check_in_date} - {self.check_out_date})"

    def clean(self):
        """Валидация:
        - Дата заезда должна быть не раньше текущей даты
        - Дата выезда должна быть позже даты заезда
        """
        if self.check_in_date < date.today():
            raise ValidationError("Дата заезда не может быть раньше текущей даты.")
        if self.check_out_date <= self.check_in_date:
            raise ValidationError("Дата выезда должна быть позже даты заезда.")
        super().clean()

    def save(self, *args, **kwargs):
        # Автоматический расчет общей стоимости на основе количества ночей
        if self.check_in_date and self.check_out_date and self.hotel:
            nights = (self.check_out_date - self.check_in_date).days
            self.total_price = nights * self.hotel.price_per_night
        super().save(*args, **kwargs)
