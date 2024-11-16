# notifications/models.py

from django.db import models
from django.conf import settings
import uuid

User = settings.AUTH_USER_MODEL

class Notification(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='notifications',
        verbose_name='Користувач'
    )
    message = models.TextField('Повідомлення')
    created_at = models.DateTimeField('Дата створення', auto_now_add=True)
    is_read = models.BooleanField('Прочитано', default=False)

    def __str__(self):
        return f"Сповіщення для {self.user.username}"

    # notifications/models.py



