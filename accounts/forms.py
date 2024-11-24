# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *  # Якщо ви використовуєте власну модель користувача

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
from phonenumber_field.formfields import PhoneNumberField
from .models import User  # Модель користувача

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        label='Електронна пошта',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'example@example.com'
        })
    )
    first_name = forms.CharField(
        required=True,
        label="Ім'я",
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше ім\'я'
        })
    )
    last_name = forms.CharField(
        required=True,
        label='Прізвище',
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваше прізвище'
        })
    )
    phone_number = PhoneNumberField(
        required=True,
        label='Номер телефону',
        region='UA',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '+380XXXXXXXXX'
        })
    )
    country = forms.CharField(
        required=True,
        label='Країна',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Україна'
        })
    )
    city = forms.CharField(
        required=True,
        label='Місто',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Київ'
        })
    )
    street = forms.CharField(
        required=True,
        label='Вулиця',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Хрещатик'
        })
    )
    building = forms.CharField(
        required=True,
        label='Будинок',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '15'
        })
    )
    postal_code = forms.CharField(
        required=True,
        label='Поштовий індекс',
        max_length=255,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '01001'
        })
    )
    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть пароль'
        })
    )
    password2 = forms.CharField(
        label="Підтвердження пароля",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Повторіть пароль'
        })
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'password1', 'password2',
            'first_name', 'last_name', 'phone_number',
            'country', 'city', 'street', 'building', 'postal_code'
        )
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ім\'я користувача'
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("Користувач з такою електронною поштою вже існує.")
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if User.objects.filter(phone_number=phone_number).exists():
            raise ValidationError("Користувач з таким номером телефону вже існує.")
        return phone_number

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise ValidationError("Користувач з таким ім'ям користувача вже існує.")
        return username


from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
import re

User = get_user_model()

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'country', 'city', 'street', 'building', 'postal_code']
        widgets = {
            'first_name': forms.TextInput(attrs={'required': 'required'}),
            'last_name': forms.TextInput(attrs={'required': 'required'}),
            'email': forms.TextInput(attrs={'required': 'required'}),
            'country': forms.TextInput(attrs={'required': 'required'}),
            'city': forms.TextInput(attrs={'required': 'required'}),
            'street': forms.TextInput(attrs={'required': 'required'}),
            'building': forms.TextInput(attrs={'required': 'required'}),
            'postal_code': forms.TextInput(attrs={'required': 'required'}),
        }
        labels = {
            'first_name': 'Ім\'я',  # змінили на "Ім'я"
            'last_name': 'Прізвище',  # змінили на "Прізвище"
            'email': 'Електронна пошта',  # змінили на "Електронна пошта"
            'phone_number': 'Номер телефону',  # якщо хочете додати
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exclude(id=self.instance.id).exists():
            raise ValidationError('Ця електронна пошта вже використовується іншим обліковим записом.')
        return email

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        # Перевірка формату номера телефону (приклад для міжнародного формату)
        if not re.match(r'^(0\d{9}|\+380\d{9})$', phone_number):
            raise ValidationError('Номер телефону повинен бути у форматі +380XXXXXXXXX або 0XXXXXXXXX.')
        # Перевірка унікальності номера телефону
        if User.objects.filter(phone_number=phone_number).exclude(id=self.instance.id).exists():
            raise ValidationError('Цей номер телефону вже використовується іншим обліковим записом.')
        return phone_number

from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomAuthenticationForm(forms.Form):
    username_or_phone = forms.CharField(
        label="Ім'я користувача або номер телефону",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'username або +380XXXXXXXXX'
        })
    )
    password = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Введіть ваш пароль'
        })
    )

    def clean(self):
        cleaned_data = super().clean()
        username_or_phone = cleaned_data.get('username_or_phone')
        password = cleaned_data.get('password')

        if username_or_phone and password:
            # Логіка аутентифікації
            user = None
            if username_or_phone.isdigit() or username_or_phone.startswith('+'):
                # Конвертація номера у формат +380XXXXXXXXX
                if username_or_phone.startswith('0') and len(username_or_phone) == 10:
                    username_or_phone = f'+380{username_or_phone[1:]}'
                try:
                    user = User.objects.get(phone_number=username_or_phone)
                except User.DoesNotExist:
                    pass
            else:
                user = authenticate(username=username_or_phone, password=password)

            if user is None or not user.check_password(password):
                raise ValidationError("Некоректне ім'я користувача/номер телефону або пароль.")

            cleaned_data['user'] = user
        return cleaned_data

    def get_user(self):
        return self.cleaned_data.get('user')
