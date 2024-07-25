from math import radians, cos, sin, sqrt, atan2

def distance_between_points(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    # Average radius of Earth in kilometers (approx.)
    avg_radius_earth_km = 6371.0  # This value can vary slightly depending on the model used

    # Calculate differences in latitude and longitude
    delta_lat = lat2_rad - lat1_rad
    delta_lon = lon2_rad - lon1_rad

    # Haversine formula to calculate distance
    a = sin(delta_lat / 2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(delta_lon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers
    distance_km = avg_radius_earth_km * c

    return distance_km