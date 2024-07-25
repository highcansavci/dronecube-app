from app.init.database import DB
from dataclasses import dataclass
from app.config import Config
from app.serialization.serialization import Serializer
from app.util.model.position_type import PositionType
from datetime import datetime, timezone, timedelta


@dataclass
class Task(DB.Model, Serializer):
    id = DB.Column(DB.Integer(), primary_key=True)
    title = DB.Column(DB.String(50), nullable=False)
    creation_date = DB.Column(DB.DateTime(timezone=True), default=datetime.now(timezone.utc).replace(tzinfo=timezone.utc), nullable=False)
    start_date = DB.Column(DB.DateTime(timezone=True), default=datetime.now(timezone.utc).replace(tzinfo=timezone.utc), nullable=False)
    end_date = DB.Column(DB.DateTime(timezone=True), default=datetime.now(timezone.utc).replace(tzinfo=timezone.utc), nullable=False)
    task_position = DB.Column(PositionType, nullable=False)
    completed = DB.Column(DB.Boolean(), default=False, nullable=False)
    images = DB.relationship("Image", backref="task", lazy="dynamic", cascade="all, delete")
    assigned_drone_id = DB.Column(DB.Integer, DB.ForeignKey('drones.id'))
    executing_drone_id = DB.Column(DB.Integer, DB.ForeignKey('drones.id'))
    assigned_drone = DB.relationship('Drone', back_populates='assigned_tasks', foreign_keys=[assigned_drone_id])
    executing_drone = DB.relationship('Drone', back_populates='executing_tasks', foreign_keys=[executing_drone_id])

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"< Task id: {self.id} - {self.title}>"

    def serialize(self):
        task_serialized = Serializer.serialize(self)
        del task_serialized["images"]
        return task_serialized
    
    def to_dict(self):
        task_dict = {
            'id': self.id,
            'title': self.title,
            'latitude': self.task_position.latitude,
            'longitude': self.task_position.longitude,
            'altitude': self.task_position.altitude,
            'creation_date': datetime.isoformat(self.creation_date),
            'start_date': datetime.isoformat(self.start_date),
            'end_date': datetime.isoformat(self.end_date),
            'completed': self.completed,
        }
        
        if self.assigned_drone_id:
            task_dict['assigned_drone_id'] = self.assigned_drone_id
            task_dict['assigned_drone_name'] = self.assigned_drone.name
            task_dict['assigned_drone_connected'] = self.assigned_drone.connected
        
        if self.executing_drone_id:
            task_dict['executing_drone_id'] = self.executing_drone_id
            task_dict['executing_drone_name'] = self.executing_drone.name
            task_dict['executing_drone_connected'] = self.executing_drone.connected    
            
        return task_dict