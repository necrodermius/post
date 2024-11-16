# config/celery.py

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Встановлюємо змінну оточення для налаштувань Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

# Читаємо налаштування з файлу settings.py
app.config_from_object('django.conf:settings', namespace='CELERY')

# Автоматичне виявлення завдань з файлів tasks.py у додатках Django
app.autodiscover_tasks()
