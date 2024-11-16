from django.contrib.auth.models import AbstractUser
from django.db import models
import uuid

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone_number = models.CharField('Номер телефону', max_length=15, blank=True, null=True)
    country = models.CharField(max_length=100, verbose_name='Країна', blank=True, null=True)
    city = models.CharField(max_length=100, verbose_name='Місто', blank=True, null=True)
    street = models.CharField(max_length=100, verbose_name='Вулиця', blank=True, null=True)
    building = models.CharField(max_length=10, verbose_name='Будинок', blank=True, null=True)
    postal_code = models.CharField(max_length=20, verbose_name='Поштовий індекс', blank=True, null=True)


    def __str__(self):
        return self.username

