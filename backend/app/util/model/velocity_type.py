from sqlalchemy import TypeDecorator, String
from app.util.model.velocity import Velocity

class VelocityType(TypeDecorator):
    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        if value is not None:
            # Convert your Position object to a database-friendly form
            return f"{value.velocity_x},{value.velocity_y},{value.velocity_z}"
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            # Convert the database value back to a Position object
            velocity_x, velocity_y, velocity_z = map(float, value.split(','))
            return Velocity(velocity_x, velocity_y, velocity_z)
        return value