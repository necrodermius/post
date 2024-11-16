# support/signals.py

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import mail_admins
from .models import SupportTicket, SupportReply

@receiver(post_save, sender=SupportTicket)
def notify_admins_new_ticket(sender, instance, created, **kwargs):
    if created:
        # Відправка сповіщення адміністраторам
        mail_admins(
            subject=f"Нова заявка в підтримку #{instance.id}",
            message=f"Користувач {instance.user.username} створив нову заявку.\n\nТема: {instance.subject}\n\nОпис:\n{instance.description}",
            fail_silently=False,
        )

@receiver(post_save, sender=SupportReply)
def update_ticket_status_on_reply(sender, instance, created, **kwargs):
    if created and instance.user.is_staff:
        # Зміна статусу заявки на "В обробці"
        instance.ticket.status = 'in_progress'
        instance.ticket.save()
