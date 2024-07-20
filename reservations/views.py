# reservations/view
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth import login, logout as django_logout, authenticate, update_session_auth_hash
from django.contrib import messages
from .models import Route, Bus, Booking, Schedule
from django.utils import timezone
import stripe
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, PasswordResetCompleteView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.db import IntegrityError
from .forms import UpdateProfileForm, CustomPasswordChangeForm,BusSearchForm


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
    form = BusSearchForm()
    return render(request, 'findbus.html', {'form': form})

@login_required
def book_seat(request, bus_id):
    bus = Bus.objects.get(id=bus_id)
    if request.method == 'POST':
          seat_numbers = request.POST.getlist('seats')
          booking = Booking.objects.create(user=request.user, bus=bus, date=date)
          for seat in seat_numbers:
              Passenger.objects.create(booking=booking, name=request.POST['name'], age=request.POST['age'], gender=request.POST['gender'])
          return redirect('booking_summary', booking_id=booking.id)
    return render(request, 'reservations/book_seat.html', {'bus': bus})


@login_required
def seebookings(request):
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'seebookings.html', {'bookings': bookings})

@login_required
def settings(request):
    if request.method == 'POST':
        profile_form = UpdateProfileForm(request.POST, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('settings')
        
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('settings')
    else:
        profile_form = UpdateProfileForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)

    return render(request, 'settings.html', {
        'profile_form': profile_form,
        'password_form': password_form
    })

@login_required
def update_profile(request):
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = UpdateProfileForm(instance=request.user)
    return render(request, 'settings.html', {'profile_form': form})

@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password has been updated successfully.')
            return redirect('settings')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CustomPasswordChangeForm(request.user)
    return render(request, 'settings.html', {'password_form': form})


def signup(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.save()
            login(request, user)
            return redirect('home')
        except IntegrityError:
            return render(request, 'signup.html', {'error': 'Email already taken'})
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
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'signin.html', {'error': 'Invalid credentials'})
    else:
        return render(request, 'signin.html')

def logout_view(request):
    django_logout(request)
    return redirect('home')

def search_results_view(request):
    if request.method == 'GET':
        form = BusSearchForm(request.GET)
        if form.is_valid():
            from_location = form.cleaned_data['from_location']
            to_location = form.cleaned_data['to_location']
            date = form.cleaned_data['date']

            print(f"Searching for buses from {from_location} to {to_location} on {date}")
            
            # Fetch routes matching the start and end points
            routes = Route.objects.filter(origin=from_location, destination=to_location)
            print(f"Found routes: {routes}")

            # Fetch schedules for the specified routes and date
            schedules = Schedule.objects.filter(
                route__origin=from_location,
                route__destination=to_location,
                date=date
            ).select_related('bus', 'route')
            print(f"Found schedules: {schedules}")

            buses = [schedule.bus for schedule in schedules]
            print(f"Found Buses: {buses}")

            return render(request, 'search_results.html', {'buses': buses, 'date': date})
        else:
            print("Form is not valid")
    else:
        form = BusSearchForm()  # Create a new instance of the form for GET request

    return render(request, 'search_results.html', {'form': form})

@login_required
def booking_summary(request, booking_id):
      booking = Booking.objects.get(id=booking_id)
      if request.method == 'POST':
          # Handle payment (integration required)
          return redirect('booking_confirmation', booking_id=booking.id)
      return render(request, 'reservations/booking_summary.html', {'booking': booking})

@login_required
def booking_confirmation(request, booking_id):
      booking = Booking.objects.get(id=booking_id)
      return render(request, 'reservations/booking_confirmation.html', {'booking': booking})

def about(request):
    return render(request, 'about.html')

def help(request):
    return render(request, 'help.html')

def faqs(request):
    return render(request, 'faqs.html')

