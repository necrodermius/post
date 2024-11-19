# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *  # Якщо ви використовуєте власну модель користувача

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, label='Електронна пошта')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['country', 'city', 'street', 'building', 'postal_code', 'email', 'first_name', 'last_name']
        widgets = {
            'country': forms.TextInput(attrs={'required': 'required'}),
            'city': forms.TextInput(attrs={'required': 'required'}),
            'street': forms.TextInput(attrs={'required': 'required'}),
            'building': forms.TextInput(attrs={'required': 'required'}),
            'postal_code': forms.TextInput(attrs={'required': 'required'}),
        }
