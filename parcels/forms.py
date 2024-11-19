from django import forms
from .models import Parcel
from accounts.models import User
from .utils import generate_unique_tracking_number

class ParcelForm(forms.ModelForm):
    recipient_username = forms.CharField(label="Ім'я користувача отримувача")

    class Meta:
        model = Parcel
        fields = ['recipient_username', 'weight', 'description']

    def clean_recipient_username(self):
        username = self.cleaned_data['recipient_username']
        try:
            recipient = User.objects.get(username=username)
        except User.DoesNotExist:
            raise forms.ValidationError("Користувача з таким ім'ям не знайдено.")
        return recipient

    def save(self, commit=True, sender=None):
        parcel = super().save(commit=False)
        parcel.sender = sender
        parcel.recipient = self.cleaned_data['recipient_username']
        # Генерація унікального трек-номера
        if not parcel.tracking_number:
            parcel.tracking_number = generate_unique_tracking_number()
        if commit:
            parcel.save()
        return parcel

    def __init__(self, *args, **kwargs):
        super(ParcelForm, self).__init__(*args, **kwargs)
        # Відфільтровуємо користувачів з неповним профілем
        required_profile_fields = ['country', 'city', 'street', 'building', 'postal_code']
        users_with_complete_profile = User.objects.all()
        for field in required_profile_fields:
            users_with_complete_profile = users_with_complete_profile.exclude(**{f"{field}__isnull": True}).exclude(
                **{f"{field}": ''})
        self.fields['recipient_username'].queryset = users_with_complete_profile.exclude(id=self.initial.get('sender_id'))

class RedirectParcelForm(forms.ModelForm):
    class Meta:
        model = Parcel
        fields = ['redirect_address']
        widgets = {
            'redirect_address': forms.TextInput(attrs={'placeholder': 'Введіть нову адресу'})
        }
