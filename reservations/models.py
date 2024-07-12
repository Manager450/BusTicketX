# reservations/models.py

from django.db import models
from django.contrib.auth.models import User

class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.origin} to {self.destination}'

class Bus(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f'Bus from {self.route.origin} to {self.route.destination} on {self.departure_time}'

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f'Booking by {self.user.username} for {self.bus}'
