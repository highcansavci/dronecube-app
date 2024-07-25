from dataclasses import dataclass
from app.serialization.serialization import Serializer


@dataclass
class Position(Serializer):
    latitude: float
    longitude: float
    altitude: float

    def serialize(self):
        position_serialized = Serializer.serialize_base(self)
        return position_serialized