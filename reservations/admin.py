# reservations/admin.py

from django.contrib import admin
from .models import Route, Bus, Booking

admin.site.register(Route)
admin.site.register(Bus)
admin.site.register(Booking)
