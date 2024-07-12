# reservations/urls.py

from django.urls import path
from . import views
from .views import (
    CustomPasswordResetView, CustomPasswordResetDoneView,
    CustomPasswordResetConfirmView, CustomPasswordResetCompleteView
)

urlpatterns = [
    path('', views.home, name='home'),
    path('findbus/', views.findbus, name='findbus'),
    path('book_seat/<int:bus_id>/', views.book_seat, name='book_seat'),
    path('seebookings/', views.seebookings, name='seebookings'),
    path('settings/', views.settings, name='settings'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('about/', views.about, name='about'),
    path('help/', views.help, name='help'),
    path('faqs/', views.faqs, name='faqs'),
    path('profile/', views.profile, name='profile'),
    path('search_results/', views.search_results_view, name='search_results'),
    path('password_reset/', CustomPasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', CustomPasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', CustomPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', CustomPasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
