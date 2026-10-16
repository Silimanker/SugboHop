from decimal import Decimal

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    phone_number = models.CharField(max_length=20, blank=True)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return self.get_username()


class Island(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    tagline = models.CharField(max_length=200)
    description = models.TextField()
    location_region = models.CharField(max_length=100, default="Cebu, Region 7")
    hero_image = models.URLField()
    ferry_duration_mins = models.IntegerField()
    rating = models.DecimalField(max_digits=3, decimal_places=2, default=Decimal("4.80"))
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Stay(models.Model):
    island = models.ForeignKey(Island, related_name="stays", on_delete=models.CASCADE)
    name = models.CharField(max_length=150)
    stay_type = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    image_url = models.URLField()

    class Meta:
        ordering = ["island", "price_per_night"]

    def __str__(self):
        return f"{self.name} ({self.island.name})"


class TransitRoute(models.Model):
    origin = models.CharField(max_length=100)
    destination_island = models.ForeignKey(
        Island, related_name="routes", on_delete=models.CASCADE
    )
    operator_name = models.CharField(max_length=100)
    departure_time = models.TimeField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        ordering = ["destination_island", "departure_time"]

    def __str__(self):
        return f"{self.origin} → {self.destination_island.name} ({self.departure_time:%H:%M})"
