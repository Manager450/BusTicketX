# reservations/admin.py

from django.contrib import admin
from .models import Route, Bus, Booking, Schedule, Passenger

admin.site.register(Route)
admin.site.register(Bus)
admin.site.register(Booking)
admin.site.register(Schedule)
admin.site.register(Passenger)