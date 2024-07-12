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
