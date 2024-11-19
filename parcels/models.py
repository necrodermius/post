# parcels/models.py

from django.db import models
from accounts.models import User
from django.conf import settings
from django.core.exceptions import ValidationError

class Parcel(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Очікує відправки'),
        ('in_sorting_center', 'У сортувальному центрі'),
        ('in_transit', 'В дорозі'),
        ('ready_for_pickup', 'Готова до отримання'),
        ('delivered', 'Доставлено'),
    ]



    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sent_parcels', on_delete=models.CASCADE, verbose_name="Відправник")
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='received_parcels', on_delete=models.CASCADE, verbose_name="Отримувач")
    tracking_number = models.CharField(max_length=100, unique=True, verbose_name="Трек-номер")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Вага")
    description = models.TextField(verbose_name="Опис", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='Очікування',
        verbose_name="Статус"
    )
    redirected = models.BooleanField(default=False, verbose_name="Переадресовано")
    redirect_address = models.CharField(max_length=255, blank=True, null=True, verbose_name="Нова адреса доставки")
    current_location = models.CharField(max_length=255, blank=True, null=True, verbose_name="Поточне місцезнаходження")
    is_paid = models.BooleanField(default=False, verbose_name="Оплачено")
    is_received = models.BooleanField(default=False, verbose_name="Отримано")
    paid_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата оплати")
    hidden_at = models.DateTimeField(null=True, blank=True, verbose_name="Дата приховування")

    def __str__(self):
        return f"Посилка {self.tracking_number} від {self.sender} до {self.recipient}"

    def __init__(self, *args, **kwargs):
        super(Parcel, self).__init__(*args, **kwargs)
        self._original_status = self.status

    def sender_address(self):
        return f"{self.sender.country}, {self.sender.city}, {self.sender.street} {self.sender.building}"

    def recipient_address(self):
        if self.redirected and self.redirect_address:
            return self.redirect_address
        else:
            return f"{self.recipient.country}, {self.recipient.city}, {self.recipient.street} {self.recipient.building}"
