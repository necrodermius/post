# Generated by Django 5.1.1 on 2024-11-16 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('parcels', '0005_parcel_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parcel',
            name='status',
            field=models.CharField(choices=[('pending', 'Очікує відправки'), ('in_sorting_center', 'У сортувальному центрі'), ('in_transit', 'В дорозі'), ('delivered', 'Доставлено')], default='pending', max_length=50, verbose_name='Статус'),
        ),
    ]