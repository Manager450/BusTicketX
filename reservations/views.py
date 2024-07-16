# reservations/view
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib import messages
from .models import Route, Bus, Booking
from django.utils import timezone
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import JsonResponse

class CustomPasswordResetView(PasswordResetView):
    template_name = 'password_reset.html'
    success_url = reverse_lazy('password_reset_done')
    email_template_name = 'password_reset_email.html'

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'password_reset_done.html'

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('password_reset_complete')

class CustomPasswordResetCompleteView(PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'profile.html', {'form': form})


def custom_404(request, exception):
    return render(request, '404.html', status=404)

@login_required
def book_seat(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    if request.method == "POST":
        booking = Booking.objects.create(user=request.user, bus=bus, date=timezone.now())
        send_mail(
            'Booking Confirmation',
            f'Your booking for the bus from {bus.route.origin} to {bus.route.destination} on {bus.departure_time} has been confirmed.',
            'from@example.com',
            [request.user.email],
            fail_silently=False,
        )
        messages.success(request, 'Seat booked successfully!')
        return redirect('seebookings')
    return render(request, 'book_seat.html', {'bus': bus})


stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def profile(request):
    return render(request, 'profile.html')

def error_404(request, exception):
    return render(request, '404.html', status=404)

@login_required
def checkout(request, booking_id):
    booking = Booking.objects.get(id=booking_id)
    if request.method == 'POST':
        try:
            charge = stripe.Charge.create(
                amount=2000,  # amount in cents
                currency='usd',
                description='Bus Ticket',
                source=request.POST['stripeToken']
            )
            messages.success(request, 'Payment successful!')
            return redirect('seebookings')
        except stripe.error.CardError as e:
            messages.error(request, 'Your card has been declined.')
    return render(request, 'checkout.html', {'booking': booking, 'stripe_key': settings.STRIPE_PUBLISHABLE_KEY})

def home(request):
    return render(request, 'home.html')

@login_required
def findbus(request):
    return render(request, 'findbus.html')

@login_required
def book_seat(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    if request.method == "POST":
        Booking.objects.create(user=request.user, bus=bus, date=timezone.now())
        messages.success(request, 'Seat booked successfully!')
        return redirect('seebookings')
    return render(request, 'book_seat.html', {'bus': bus})

@login_required
def seebookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'seebookings.html', {'bookings': bookings})

@login_required
def settings(request):
    if request.method == 'POST':
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
    else:
        password_form = PasswordChangeForm(request.user)
    return render(request, 'settings.html', {'password_form': password_form})

def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            login(request, user)  # Log the user in after creation
            messages.success(request, 'Account created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Passwords do not match!')
            return render(request, 'signup.html')
    else:
        return render(request, 'signup.html')

def get_user_info(request, email, password):

    user = authenticate(request, username=email, password=password)

    if user is not None:
        return JsonResponse(user)
    else:
        messages.error(request, 'Invalid email or password!')


def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Invalid email or password!')
        else:
            messages.error(request, 'Invalid email or password!')
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def logout(request):
    logout(request)
    return redirect('home')

def search_results_view(request):
       from_location = request.GET['from']
       to_location = request.GET['to']
       date_of_journey = request.GET['date_of_journey']
       return_date = request.GET['return_date']
       context = {
           'from': from_location,
           'to': to_location,
           'date_of_journey': date_of_journey,
           'return_date': return_date,
       }
       return render(request, 'search_results.html', context)

def about(request):
    return render(request, 'about.html')

def help(request):
    return render(request, 'help.html')

def faqs(request):
    return render(request, 'faqs.html')

