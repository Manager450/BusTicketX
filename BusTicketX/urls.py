# BusTicketX/urls.py

from django.contrib import admin
from django.urls import path, include

handler404 = 'reservations.views.custom_404'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('reservations.urls')),
]
