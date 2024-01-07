from geopy.distance import geodesic

from .services import get_all_chargers


def nearest_point(initial_point):
    nearest_point = None
    nearest_distance = float('inf')
    chargers = get_all_chargers()
    for charger in chargers:
        point = (charger['latitude'], charger['longitude'])
        distance = geodesic(initial_point, point).kilometers
        if distance < nearest_distance:
            nearest_distance = distance
            nearest_point = charger['charger_id']
    return nearest_point