from dataclasses import dataclass
from app.auth.model.user import User
from app.serialization.serialization import Serializer
from app.init.database import DB
from app.util.model.position_type import PositionType
from app.util.model.velocity_type import VelocityType

@dataclass
class Drone(DB.Model, Serializer):
    __tablename__ = 'drones'

    id = DB.Column(DB.Integer(), primary_key=True)
    name = DB.Column(DB.String(50), nullable=False)
    global_position = DB.Column(PositionType, nullable=False)
    home_position = DB.Column(PositionType, nullable=False)
    velocity = DB.Column(VelocityType, nullable=False)
    connected = DB.Column(DB.Boolean(), default=False, nullable=False)
    assigned_tasks = DB.relationship('Task', back_populates='assigned_drone', foreign_keys='Task.assigned_drone_id')
    executing_tasks = DB.relationship('Task', back_populates='executing_drone', foreign_keys='Task.executing_drone_id')  
    users = DB.relationship('User', secondary="user_drones", lazy="dynamic", back_populates='drones')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"< Drone info: {self.id} - {self.name}>"

    def serialize(self):
        drone_serialized = Serializer.serialize(self)
        del drone_serialized["assigned_tasks"]
        del drone_serialized["executing_tasks"]
        del drone_serialized["users"]
        return drone_serialized

    def to_dict(self):
        drone_dict = {
            'id': self.id,
            'name': self.name,
            'latitude': self.global_position.latitude,
            'longitude': self.global_position.longitude,
            'altitude': self.global_position.altitude,
            'home_latitude': self.home_position.latitude,
            'home_longitude': self.home_position.longitude,
            'home_altitude': self.home_position.altitude,
            'velocity_x': self.velocity.velocity_x,
            'velocity_y': self.velocity.velocity_y,
            'velocity_z': self.velocity.velocity_z,
            'connected': self.connected,
        }
        return drone_dict


user_drones = DB.Table(
    "user_drones",
    DB.Column("user_id", DB.Integer, DB.ForeignKey(User.__tablename__ + ".id")),
    DB.Column("drone_id", DB.Integer, DB.ForeignKey(Drone.__tablename__ + ".id")),
)
