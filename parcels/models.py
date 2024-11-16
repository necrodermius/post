from django.db import models
from accounts.models import User
import uuid

class Parcel(models.Model):
    id = models.UUIDField(default=uuid.uuid4, editable=False)
    sender = models.ForeignKey(User, related_name='sent_parcels', on_delete=models.CASCADE, verbose_name="Відправник")
    recipient = models.ForeignKey(User, related_name='received_parcels', on_delete=models.CASCADE, verbose_name="Отримувач", null=True)
    tracking_number = models.CharField(primary_key=True, default=uuid.uuid4, editable=False, max_length=100, unique=True, verbose_name="Трек-номер")
    weight = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Вага")
    description = models.TextField(verbose_name="Опис", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата створення")
    STATUS_CHOICES = [
        ('pending', 'Очікує відправки'),
        ('in_sorting_center', 'У сортувальному центрі'),
        ('in_transit', 'В дорозі'),
        ('delivered', 'Доставлено'),
    ]
    status = models.CharField(
        max_length=50,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name="Статус"
    )

    def sender_address(self):
        return f"{self.sender.country}, {self.sender.city}, {self.sender.street} {self.sender.building}"

    def recipient_address(self):
        return f"{self.recipient.country}, {self.recipient.city}, {self.recipient.street} {self.recipient.building}"

    def __init__(self, *args, **kwargs):
        super(Parcel, self).__init__(*args, **kwargs)
        self._original_status = self.status

    def __str__(self):
        return f"Посилка {self.tracking_number} від {self.sender} до {self.recipient}"
