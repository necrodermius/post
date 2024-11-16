from django import forms
from .models import Parcel
from accounts.models import User

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
