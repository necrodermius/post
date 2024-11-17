# Generated by Django 5.1.1 on 2024-11-17 03:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='parcel',
            name='hidden_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата приховування'),
        ),
        migrations.AddField(
            model_name='parcel',
            name='is_paid',
            field=models.BooleanField(default=False, verbose_name='Оплачено'),
        ),
        migrations.AddField(
            model_name='parcel',
            name='is_received',
            field=models.BooleanField(default=False, verbose_name='Отримано'),
        ),
        migrations.AddField(
            model_name='parcel',
            name='paid_at',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Дата оплати'),
        ),
    ]
