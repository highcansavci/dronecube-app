from sqlalchemy import TypeDecorator, String
from app.util.model.position import Position

class PositionType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            return f"{value.latitude},{value.longitude},{value.altitude}"
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            latitude, longitude, altitude = map(float, value.split(','))
            return Position(latitude, longitude, altitude)
        return value