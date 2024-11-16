# payments/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Payment

@receiver(post_save, sender=Payment)
def handle_payment_update(sender, instance, created, **kwargs):
    # Якщо платіж новий і статус 'completed', або статус змінено на 'completed'
    if (created and instance.status == 'completed') or (not created and instance.status == 'completed' and instance._pre_status != 'completed'):
        # Відправка квитанції
        send_mail(
            'Квитанція про оплату',
            f'Ваш платіж на суму {instance.amount} успішно завершено.\nДякуємо за користування нашими послугами!',
            'no-reply@example.com',
            [instance.user.email],
            fail_silently=False,
        )

@receiver(post_save, sender=Payment)
def save_previous_status(sender, instance, **kwargs):
    # Збереження попереднього статусу для перевірки змін
    instance._pre_status = instance.status
