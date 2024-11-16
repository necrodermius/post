# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *  # Якщо ви використовуєте власну модель користувача

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Електронна пошта')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'country', 'city', 'street', 'building', 'postal_code']

