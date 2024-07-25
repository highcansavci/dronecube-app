import datetime
import json
from app.init.database import DB
from app.init.minio_client import MINIO_CLIENT
from app.config import Config
from app.image.model.image import Image
from app.image.service.image_service import ImageService


class ImageServiceImpl(ImageService):
    # Singleton Service
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def serialize_images(self, task):
        image_serialize_list = Image.serialize_list(task.images)
        for image_serialized in image_serialize_list:
            image_serialized["task_id"] = task.id
            image_serialized["task_title"] = task.title
            image_serialized["task_date"] = task.date
            image_serialized["task_completed"] = task.completed
        return json.dumps(image_serialize_list, default=lambda obj: obj.isoformat())
    
    def get_image(self, task, image_id):
        return task.images.filter_by(id=image_id).first()
    
    def get_image_url(self, filename):
        MINIO_CLIENT.get_presigned_url("GET", Config.MINIO_BUCKET, filename, expires=datetime.timedelta(hours=2))          