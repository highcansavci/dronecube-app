from sqlalchemy.orm import Mapped
from app.init.database import DB
from datetime import datetime
from dataclasses import dataclass
from datetime import datetime, timezone, timedelta
from app.config import Config
from app.serialization.serialization import Serializer

@dataclass
class Image(DB.Model, Serializer):
    id = DB.Column(DB.Integer(), primary_key=True)
    date = DB.Column(DB.DateTime(timezone=True), default=datetime.now(tz=timezone(timedelta(hours=Config.UTC))), nullable=False)
    filename = DB.Column(DB.String(50), nullable=False)
    task_id = DB.Column(DB.Integer(), DB.ForeignKey('task.id', ondelete="CASCADE"), nullable=False)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __repr__(self):
        return f"< Image taken: {self.id} - {self.date}>"

    def serialize(self):
        image_serialized = Serializer.serialize(self)
        del image_serialized["task"]
        return image_serialized