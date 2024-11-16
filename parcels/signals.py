# parcels/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Parcel
from django.core.mail import send_mail

@receiver(post_save, sender=Parcel)
def parcel_status_updated(sender, instance, created, **kwargs):
    if not created:
        # Отримуємо попереднє значення статусу
        old_instance = Parcel.objects.get(pk=instance.pk)
        old_status = old_instance.status
        new_status = instance.status

        if old_status != new_status:
            # Діємо в залежності від нового статусу
            if new_status == 'Доставлено':
                # Відправляємо повідомлення отримувачу
                send_mail(
                    'Ваша посилка доставлена',
                    f'Посилка з трек-номером {instance.tracking_number} була доставлена.',
                    [instance.sender.email],
                    [instance.recipient.email],
                    fail_silently=False,
                )
