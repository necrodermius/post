# parcels/utils.py

import uuid

def generate_unique_tracking_number():
    return str(uuid.uuid4())

from geopy.geocoders import Nominatim
from geopy.distance import geodesic


import logging
import geopy.distance

geolocator = Nominatim(user_agent="parcel_delivery_app")
logger = logging.getLogger(__name__)

def calculate_distance(address1, address2):
    # Геокодування адрес
    coords_1 = geocode_address(address1)
    coords_2 = geocode_address(address2)

    logger.info(f"Геокодовані координати для '{address1}': {coords_1}")
    logger.info(f"Геокодовані координати для '{address2}': {coords_2}")

    if coords_1 and coords_2:
        distance = geopy.distance.distance(coords_1, coords_2).km
        logger.info(f"Обчислена відстань між '{address1}' та '{address2}': {distance} км")
        return distance
    else:
        logger.error("Не вдалося геокодувати одну або обидві адреси.")
        return 0  # Або інше значення за замовчуванням

from geopy.geocoders import Nominatim

geolocator = Nominatim(user_agent="your_app_name")

def geocode_address(address):
    try:
        location = geolocator.geocode(address)
        if location:
            logger.info(f"Геокодовано адресу '{address}' до координат ({location.latitude}, {location.longitude})")
            return (location.latitude, location.longitude)
        else:
            logger.error(f"Не вдалося геокодувати адресу '{address}'")
            return None
    except Exception as e:
        logger.exception(f"Помилка при геокодуванні адреси '{address}': {e}")
        return None

def calculate_delivery_time(distance):
    # Припустимо, що середня швидкість доставки 50 км/год
    average_speed = 50  # км/год

    if distance <= 0:
        logger.warning(f"Некоректна відстань: {distance}. Встановлено мінімальний час доставки 60 секунд.")
        return 60  # Мінімальний час доставки в секундах

    time_in_hours = distance / average_speed
    time_in_seconds = time_in_hours * 3600  # Перетворення годин у секунди

    logger.info(f"Час доставки для відстані {distance} км: {time_in_seconds} секунд")

    return int(time_in_seconds)
