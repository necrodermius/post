from django.db import models
from django.conf import settings
import uuid

class Payment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    PAYMENT_METHODS = (
        ('card', 'Картка'),
        ('paypal', 'PayPal'),
        ('cash', 'Готівка'),
    )
    PAYMENT_STATUSES = (
        ('pending', 'Очікується'),
        ('completed', 'Завершено'),
        ('failed', 'Неуспішно'),
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Користувач'
    )
    amount = models.DecimalField('Сума', max_digits=10, decimal_places=2)
    payment_method = models.CharField('Метод оплати', max_length=50, choices=PAYMENT_METHODS)
    timestamp = models.DateTimeField('Час платежу', auto_now_add=True)
    status = models.CharField('Статус', max_length=20, choices=PAYMENT_STATUSES, default='pending')
    transaction_id = models.CharField('ID транзакції', max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount} грн - {self.get_status_display()}"
