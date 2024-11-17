# parcels/tasks.py

import logging

from celery import shared_task
from .models import Parcel
from .utils import calculate_distance, calculate_delivery_time
import logging

logger = logging.getLogger(__name__)

@shared_task
def update_parcel_status(parcel_id, new_status):
    logger.info(f"Оновлення статусу посилки {parcel_id} до {new_status}")
    try:
        parcel = Parcel.objects.get(id=parcel_id)
        parcel.status = new_status
        parcel.save()
        logger.info(f"Статус посилки {parcel_id} оновлено до {new_status}")
    except Parcel.DoesNotExist:
        logger.error(f"Посилка {parcel_id} не існує.")

@shared_task
def process_parcel(parcel_id):
    logger.info(f"Обробка посилки {parcel_id}")
    try:
        parcel = Parcel.objects.get(id=parcel_id)
        # Оновлення статусу на 'in_sorting_center'
        update_parcel_status.delay(parcel_id, 'in_sorting_center')
        logger.info(f"Статус посилки {parcel_id} встановлено на 'in_sorting_center'")

        # Обчислення відстані та часу доставки
        sender_address = parcel.sender_address()
        recipient_address = parcel.recipient_address()
        distance = calculate_distance(sender_address, recipient_address)
        delivery_time = calculate_delivery_time(distance)
        logger.info(f"Розрахований час доставки для посилки {parcel_id}: {delivery_time} секунд")

        # Оновлення статусу на 'in_transit'
        update_parcel_status.delay(parcel_id, 'in_transit')
        logger.info(f"Статус посилки {parcel_id} встановлено на 'in_transit'")

        # Запланувати зміну статусу на 'delivered'
        update_parcel_status.apply_async(
            (parcel_id, 'delivered'), countdown=delivery_time
        )
        logger.info(f"Заплановано зміну статусу посилки {parcel_id} на 'delivered' через {delivery_time} секунд")
    except Parcel.DoesNotExist:
        logger.error(f"Посилка {parcel_id} не існує.")
    except Exception as e:
        logger.exception(f"Сталася помилка під час обробки посилки {parcel_id}: {e}")



@shared_task
def process_redirected_parcel(parcel_id):
    try:
        parcel = Parcel.objects.get(id=parcel_id)
        logger.info(f"Обробка переадресованої посилки {parcel_id}")

        # Визначаємо поточну локацію
        if parcel.status == 'delivered':
            current_address = parcel.recipient_address()
        elif parcel.current_location:
            current_address = parcel.current_location
        else:
            current_address = "Сортувальний центр"  # Або інша логіка

        # Обчислення відстані та часу доставки до нової адреси
        new_destination = parcel.redirect_address
        distance = calculate_distance(current_address, new_destination)
        delivery_time = calculate_delivery_time(distance)

        logger.info(f"Розрахований час доставки для переадресованої посилки {parcel_id}: {delivery_time} секунд")

        # Оновлення статусу на 'in_transit'
        update_parcel_status.delay(parcel_id, 'in_transit')

        # Запланувати зміну статусу на 'delivered' після часу доставки
        update_parcel_status.apply_async(
            (parcel_id, 'delivered'), countdown=delivery_time
        )
        logger.info(f"Заплановано зміну статусу посилки {parcel_id} на 'delivered' через {delivery_time} секунд")
    except Parcel.DoesNotExist:
        logger.error(f"Посилка {parcel_id} не існує.")
    except Exception as e:
        logger.exception(f"Сталася помилка під час обробки переадресованої посилки {parcel_id}: {e}")
