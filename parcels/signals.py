# parcels/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import Parcel

from accounts.admin_logging import admin_log     # ← імпорт нашого декоратора


@receiver(post_save, sender=Parcel)
@admin_log(
    "{instance} status changed to '{instance.status}' "
    "and notification email sent to {instance.recipient.email}"
)
def parcel_status_updated(sender, instance, created, **kwargs):
    """
    Надсилаємо листа отримувачу, якщо статус посилки змінився на «Доставлено».
    Декоратор створює LogEntry у django‑admin із повідомленням вище.
    """
    if created:
        return                      # нову посилку ще не доставляємо

    # одержуємо попередній статус
    old_status = (
        Parcel.objects.filter(pk=instance.pk)
        .values_list("status", flat=True)
        .first()
    )

    if old_status == instance.status:
        return                      # статус не змінився

    if instance.status == "Доставлено":
        send_mail(
            "Ваша посилка доставлена",
            f"Посилка з трек‑номером {instance.tracking_number} була доставлена.",
            [instance.sender.email],
            [instance.recipient.email],
            fail_silently=False,
        )
