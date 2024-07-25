from math import radians, degrees, sin, cos, atan2, sqrt, acos, pi

def slerp(start_lat, start_lon, end_lat, end_lon, fraction):
    start_lat, start_lon, end_lat, end_lon = map(radians, [start_lat, start_lon, end_lat, end_lon])
    
    delta_lon = end_lon - start_lon

    cos_start_lat = cos(start_lat)
    cos_end_lat = cos(end_lat)

    sin_start_lat = sin(start_lat)
    sin_end_lat = sin(end_lat)
    
    a = cos_end_lat * cos(delta_lon)
    b = cos_start_lat * sin_end_lat - sin_start_lat * cos_end_lat * cos(delta_lon)
    c = sqrt((cos_end_lat * sin(delta_lon)) ** 2 + b ** 2)
    
    d = atan2(c, a)
    f = sin((1 - fraction) * d) / sin(d)
    g = sin(fraction * d) / sin(d)
    
    x = f * cos_start_lat * cos_start_lat + g * cos_end_lat * cos_end_lat
    y = f * cos_start_lat * sin(start_lon) + g * cos_end_lat * sin(end_lon)
    
    lat = atan2(x, y)
    lon = start_lon + atan2(g * sin(delta_lon) * cos_end_lat, f * cos_start_lat + g * cos_end_lat * cos(delta_lon))
    
    return degrees(lat), degrees(lon)