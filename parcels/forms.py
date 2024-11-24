from django import forms
from .models import Parcel
from accounts.models import User
from .utils import generate_unique_tracking_number

from django import forms
from .models import Parcel
from accounts.models import User

from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from .models import Parcel
from .utils import generate_unique_tracking_number

User = get_user_model()

class ParcelForm(forms.ModelForm):
    recipient_identifier = forms.CharField(
        label="Ім'я користувача або номер телефону отримувача",
        widget=forms.TextInput(attrs={
            'placeholder': 'Введіть ім\'я користувача або номер телефону отримувача',
            'class': 'form-control'
        })
    )
    weight = forms.DecimalField(
        label="Вага (кг)",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Наприклад: 1.5',
            'class': 'form-control'
        })
    )
    description = forms.CharField(
        label="Опис посилки",
        required=False,
        widget=forms.Textarea(attrs={
            'placeholder': 'Короткий опис вмісту посилки',
            'class': 'form-control',
            'rows': 3
        })
    )
    custom_address = forms.BooleanField(
        required=False,
        label="Відправити на іншу адресу",
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        })
    )
    custom_recipient_address = forms.CharField(
        required=False,
        label="Нова адреса отримувача",
        widget=forms.TextInput(attrs={
            'placeholder': 'Наприклад: Україна, Київ, вул. Хрещатик 1',
            'class': 'form-control'
        })
    )

    class Meta:
        model = Parcel
        fields = ['recipient_identifier', 'weight', 'description', 'custom_address', 'custom_recipient_address']

    def clean(self):
        cleaned_data = super().clean()
        custom_address = cleaned_data.get('custom_address')
        custom_recipient_address = cleaned_data.get('custom_recipient_address')

        if custom_address and not custom_recipient_address:
            raise forms.ValidationError("Якщо обрано 'Відправити на іншу адресу', потрібно вказати нову адресу.")
        return cleaned_data

    def clean_recipient_identifier(self):
        identifier = self.cleaned_data['recipient_identifier']
        recipient = None

        # Перевіряємо, чи це номер телефону
        if identifier.isdigit() or identifier.startswith('+'):
            # Нормалізуємо номер телефону
            phone_number = identifier
            if phone_number.startswith('0') and len(phone_number) == 10:
                phone_number = f'+380{phone_number[1:]}'
            # Пошук користувача за номером телефону
            try:
                recipient = User.objects.get(phone_number=phone_number)
            except User.DoesNotExist:
                pass
        else:
            # Пошук користувача за ім'ям користувача
            try:
                recipient = User.objects.get(username=identifier)
            except User.DoesNotExist:
                pass

        if recipient is None:
            raise forms.ValidationError("Користувача з таким ім'ям або номером телефону не знайдено.")
        return recipient

    def save(self, commit=True, sender=None):
        parcel = super().save(commit=False)
        parcel.sender = sender
        parcel.recipient = self.cleaned_data['recipient_identifier']
        # Генерація унікального трек-номера
        if not parcel.tracking_number:
            parcel.tracking_number = generate_unique_tracking_number()
        if commit:
            parcel.save()
        return parcel


class RedirectParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ['redirect_address']
        widgets = {
            'redirect_address': forms.TextInput(attrs={'placeholder': 'Введіть нову адресу'})
        }
