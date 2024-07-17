# reservations/forms.py

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm
from django.contrib.auth.models import User

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class SignInForm(AuthenticationForm):
    username = forms.CharField(max_length=254, required=True)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

class PasswordResetForm(forms.Form):
    email = forms.EmailField(max_length=254, required=True)

class UpdateProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password1'].widget.attrs.update({'class': 'form-control'})
        self.fields['new_password2'].widget.attrs.update({'class': 'form-control'})

class BusSearchForm(forms.Form):
    LOCATIONS = [
        ('Accra', 'Accra'),
        ('Kumasi', 'Kumasi'),
        ('Cape Coast', 'Cape Coast'),
        ('Tamale', 'Tamale'),
        ('Ho', 'Ho'),
        ('Takoradi', 'Takoradi'),
        ('Koforidua', 'Koforidua'),
        ('Sunyani', 'Sunyani'),
        ('Wa', 'Wa'),
        ('Bolgatanga', 'Bolgatanga'),
        ('Damongo', 'Damongo'),
        ('Techiman', 'Techiman'),
        ('Dambai', 'Dambai'),
        ('Goaso', 'Goaso'),
        ('Sefwi Wiaso', 'Sefwi Wiaso'),
        ('Nalerigu', 'Nalerigu'),
    ]

    from_location = forms.ChoiceField(choices= LOCATIONS, label="From")
    to_location = forms.ChoiceField(choices=LOCATIONS, label="To")
    date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))