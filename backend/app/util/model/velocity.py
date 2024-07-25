from dataclasses import dataclass
from app.serialization.serialization import Serializer


@dataclass
class Velocity(Serializer):
    velocity_x: float
    velocity_y: float
    velocity_z: float

    def serialize(self):
        velocity_serialized = Serializer.serialize_base(self)
        return velocity_serialized