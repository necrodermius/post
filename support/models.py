# support/models.py

from django.db import models
from django.conf import settings
import uuid

class SupportTicket(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    STATUS_CHOICES = (
        ('open', 'Відкрито'),
        ('in_progress', 'В обробці'),
        ('closed', 'Закрито'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='support_tickets',
        verbose_name='Користувач'
    )
    subject = models.CharField('Тема', max_length=255)
    description = models.TextField('Опис')
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=STATUS_CHOICES, default='open')

    def __str__(self):
        return f"Тікет #{self.id} - {self.subject}"

class SupportReply(models.Model):
    ticket = models.ForeignKey(
        SupportTicket,
        on_delete=models.CASCADE,
        related_name='replies',
        verbose_name='Тікет'
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Користувач'
    )
    message = models.TextField('Повідомлення')
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)

    def __str__(self):
        return f"Відповідь на тікет #{self.ticket.id}"
