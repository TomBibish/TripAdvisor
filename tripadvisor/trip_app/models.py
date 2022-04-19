from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Country(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)

    def __str__(self):
        return f"{self.name}"


class City(models.Model):
    city = models.CharField(max_length=32, null=False, blank=False)

    def __str__(self):
        return f"{self.city}"


class RestaurantType(models.Model):
    name = models.CharField(max_length=32,null=False, blank=False)

    def __str__(self):
        return f"{self.name}"


class Restaurant(models.Model):
    STARS_CHOICES = (
        ('$', '$'),
        ('$$', '$$'),
        ('$$$', '$$$'),
    )
    name = models.CharField(max_length=128, null=False, blank=False)
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    city = models.ForeignKey(City, on_delete=models.RESTRICT)
    address = models.CharField(max_length=128, null=True, blank=True)
    type = models.ForeignKey(RestaurantType, on_delete=models.RESTRICT)
    price_range = models.CharField(max_length=3, choices=STARS_CHOICES)
    image = models.URLField(default="", null=True, blank=True)

    def __str__(self):
        return f"{self.name} restaurant, {self.city}, {self.country}"


class Review(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.RESTRICT)
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    STARS_CHOICES = (
        ('1', '1 STARS'),
        ('2', '2 STARS'),
        ('3', '3 STARS'),
        ('4', '4 STARS'),
        ('5', '5 STARS')
    )
    stars = models.CharField(max_length=1, choices=STARS_CHOICES)
    review_title = models.CharField(max_length=128, null=False, blank=False)
    review_text = models.CharField(max_length=528, null=True, blank=True)
    visit_date = models.DateField()

    def __str__(self):
        return f"{self.stars} Stars Review from {self.user} to {self.restaurant}"


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.RESTRICT)
    image = models.URLField(default="")
    birth_date = models.DateField()
    country = models.ForeignKey(Country, on_delete=models.RESTRICT)
    city = models.ForeignKey(City, on_delete=models.RESTRICT)
    address = models.CharField(max_length=128, null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}"
