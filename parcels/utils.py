# parcels/utils.py

import uuid

def generate_unique_tracking_number():
    return str(uuid.uuid4())

from geopy.geocoders import Nominatim
from geopy.distance import geodesic

geolocator = Nominatim(user_agent="parcel_delivery_app")

def calculate_distance(address1, address2):
    location1 = geolocator.geocode(address1)
    location2 = geolocator.geocode(address2)

    if not location1 or not location2:
        raise ValueError("Не вдалося геокодувати одну або обидві адреси.")

    coords_1 = (location1.latitude, location1.longitude)
    coords_2 = (location2.latitude, location2.longitude)

    distance = geodesic(coords_1, coords_2).kilometers
    return distance

def calculate_delivery_time(distance):
    if distance is None or distance == 0:
        raise ValueError("Недійсна відстань для розрахунку часу доставки.")
    # Припустимо, що середня швидкість доставки 60 км/год
    delivery_time_hours = distance / 60
    # Перетворюємо години у секунди
    return int(delivery_time_hours * 3600)
