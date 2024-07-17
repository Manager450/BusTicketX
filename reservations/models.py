# reservations/models.py

from django.db import models
from django.contrib.auth.models import User

class Route(models.Model):
    origin = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.origin} to {self.destination}'

class Bus(models.Model):
    operator = models.CharField(max_length=100)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    departure_time = models.DateTimeField()
    available_seats = models.IntegerField()

    def __str__(self):
        return f'Bus from {self.route.origin} to {self.route.destination} on {self.departure_time}'
    
class Schedule(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    date = models.DateField()
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    available_seats = models.IntegerField()
    fare = models.DecimalField(max_digits=6,decimal_places=2)

    def __str__(self):
        return f"{self.bus.operator} on {self.route} at {self.departure_time}"


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE)
    date = models.DateTimeField()

    def __str__(self):
        return f'Booking by {self.user.username} for {self.bus}'
    
class Passenger(models.Model):
    booking = models.ForeignKey(Booking, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    age = models.PositiveBigIntegerField()
    gender = models.CharField(max_length=10)

    def __str__(self):
        return self.name