# accounts/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from .models import User
from parcels.models import Parcel

@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        # Відправка вітального електронного листа
        send_mail(
            'Ласкаво просимо до нашого поштового сервісу!',
            'Дякуємо за реєстрацію в нашому сервісі. Ми раді вітати вас!',
            'maksym.putin.django@gmail.com',  # Замість цього вкажіть вашу електронну адресу
            [instance.email],
            fail_silently=False,
        )

# parcels/signals.py

@receiver(post_save, sender=Parcel)
def parcel_status_updated(sender, instance, created, **kwargs):
    if not created:
        if instance._original_status != instance.status:
            # Статус змінився
            new_status = instance.status
            if new_status == 'Доставлено':
                # Виконуємо потрібні дії
                pass
        # Оновлюємо початковий статус
        instance._original_status = instance.status
