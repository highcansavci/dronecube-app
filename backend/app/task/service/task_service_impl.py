from datetime import datetime, timezone, timedelta
from io import BytesIO
import json
import numpy as np
from werkzeug.utils import secure_filename
from PIL import Image as Image_
from app.init.database import DB
from app.init.minio_client import MINIO_CLIENT
from app.config import Config
from app.image.model.image import Image
from app.task.model.task import Task
from app.task.service.task_service import TaskService
from app.util.model.position import Position
from flask import current_app
from sqlalchemy import func, and_, cast, Float
import math


class TaskServiceImpl(TaskService):
    # Singleton Service
    _instance = None
        
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TaskServiceImpl, cls).__new__(cls)
        return cls._instance
        
    def get_current_user(self):
        return current_app.drone_service.get_current_user()
    
    def query_drone(self, drone_id):
        return current_app.drone_service.query_drone(drone_id)  
    
    def serialize_task(self, task):
        task_serialized = Task.serialize(task)
        if task_serialized["assigned_drone"]:
            if self.get_current_user() not in task_serialized["assigned_drone"].users:
                return json.dumps({})
            task_serialized["assigned_drone_id"] = task_serialized["assigned_drone"].id
            task_serialized["assigned_drone_name"] = task_serialized["assigned_drone"].name
            task_serialized["assigned_drone_connected"] = task_serialized["assigned_drone"].connected
            del task_serialized["assigned_drone"]
        if task_serialized["executing_drone"]:
            if self.get_current_user() not in task_serialized["executing_drone"].users:
                return json.dumps({})
            task_serialized["executing_drone_id"] = task_serialized["executing_drone"].id
            task_serialized["executing_drone_name"] = task_serialized["executing_drone"].name
            task_serialized["executing_drone_connected"] = task_serialized["executing_drone"].connected
            del task_serialized["executing_drone"]
        return json.dumps(task_serialized, default=lambda obj: obj.isoformat())
    
    def serialize_all_tasks(self, tasks):
        task_serialize_list = Task.serialize_list(tasks)
        for task_serialized in task_serialize_list:
            if task_serialized["assigned_drone"]:
                if self.get_current_user() not in task_serialized["assigned_drone"].users:
                    return json.dumps({})
                task_serialized["assigned_drone_id"] = task_serialized["assigned_drone"].id
                task_serialized["assigned_drone_name"] = task_serialized["assigned_drone"].name
                task_serialized["assigned_drone_connected"] = task_serialized["assigned_drone"].connected
                del task_serialized["assigned_drone"]
            if task_serialized["executing_drone"]:
                if self.get_current_user() not in task_serialized["executing_drone"].users:
                    return json.dumps({})
                task_serialized["executing_drone_id"] = task_serialized["executing_drone"].id
                task_serialized["executing_drone_name"] = task_serialized["executing_drone"].name
                task_serialized["executing_drone_connected"] = task_serialized["executing_drone"].connected
                del task_serialized["executing_drone"]
        return json.dumps(task_serialize_list, default=lambda obj: obj.isoformat())
    
    def __make_timezone_aware(self, date_str):
        naive_datetime = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        return naive_datetime.replace(tzinfo=timezone.utc).astimezone(timezone(timedelta(hours=Config.UTC)))
    
    def create_task(self, form, drone):
        task_position = Position(float(form.latitude.data), float(form.longitude.data), float(form.altitude.data))
        task = Task(title=form.title.data,
                    start_date=self.__make_timezone_aware(form.start_date.data),
                    end_date=self.__make_timezone_aware(form.end_date.data),
                    completed=form.completed.data == "Completed",
                    task_position=task_position,
                    assigned_drone_id=drone.id if drone else None,
                    images=list())
        DB.session.add(task)
        DB.session.commit()
        return self.serialize_task(task)
        
    def get_all_tasks(self):
        return DB.session.query(Task).all()   
    
    def get_task(self, task_id):
        return DB.session.query(Task).get(task_id)
    
    def update_task(self, data, task):
        task.title = task.title if data.get("title") == "" else data.get('title')
        task.start_date = task.start_date if data.get("start_date") == 'null' else self.__make_timezone_aware(data.get("start_date"))
        task.end_date = task.end_date if data.get("end_date") == 'null' else self.__make_timezone_aware(data.get("end_date"))
        task.completed = task.completed == "Completed" if data.get('completed') == 'null' else data.get('completed') == "Completed"
        latitude = task.task_position.latitude if data.get("latitude") == "null" else data.get("latitude")
        longitude = task.task_position.longitude if data.get("longitude") == "null" else data.get("longitude")
        altitude = task.task_position.altitude if data.get("altitude") == "null" else data.get("altitude")
        task_position = Position(latitude, longitude, altitude)
        task.task_position = task_position
        DB.session.commit()
        return self.serialize_task(task)
    
    def delete_task(self, task):
        DB.session.delete(task)
        DB.session.commit()
        
    def execute_task(self, task, task_id):
        self.__take_images(task_id, task)
        self.complete_task(task)  
        
    def __create_image_buffer(self, task_id, task, i):
        pixels = np.uint8(np.random.randint(0, 256, size=(Config.IMAGE_WIDTH, Config.IMAGE_HEIGHT, Config.IMAGE_CHANNEL)))
        image = Image_.fromarray(pixels)
        filename = secure_filename(str(task_id) + "_" + str(task.title) + "_" + str(task.date) + "_" + str(task.drone_id) + "_" + str(i) + ".png")
        image_buffer = BytesIO()
        image.save(image_buffer, format='PNG')
        image_buffer.seek(0)   
        return filename, image_buffer   
    
    def save_image(self, filename, task_id):
        img = Image(filename=filename, task_id=task_id)
        DB.session.add(img)  
    
    def __create_minio_bucket():
        found = MINIO_CLIENT.bucket_exists(Config.MINIO_BUCKET)
        if not found:
            MINIO_CLIENT.make_bucket(Config.MINIO_BUCKET)
     
    def __save_image_on_minio_bucket(filename, image_buffer):
        try:
            MINIO_CLIENT.put_object(Config.MINIO_BUCKET, filename, image_buffer, len(image_buffer.getvalue()))
        except Exception as e:
            print(e)        
        
    def __take_images(self, task_id, task):
        for i in range(Config.NUM_IMAGES):
            filename, image_buffer = self.__create_image_buffer(task_id, task, i)
            self.save_image(filename, task_id)
            self.__create_minio_bucket()
            self.__save_image_on_minio_bucket(filename, image_buffer)
            
    def complete_task(self, task):
        task.completed = True
        DB.session.commit()    
        
    def filter_all_tasks_socket(self, dict_, websocket):
        filters = []
        title = dict_.get("title")
        if title:
            filters.append(Task.title == title)
        
        filter_fields = {
            'latitude': ('task_position', 1),
            'longitude': ('task_position', 2),
            'altitude': ('task_position', 3)
        }
        
        for field, (column_name, part) in filter_fields.items():
            min_value = float(dict_.get(f"{field}_min", math.nan))
            max_value = float(dict_.get(f"{field}_max", math.nan))
            
            if not math.isnan(min_value):
                filters.append(cast(func.split_part(getattr(Task, column_name), ',', part), Float) >= min_value)
            if not math.isnan(max_value):
                filters.append(cast(func.split_part(getattr(Task, column_name), ',', part), Float) <= max_value)
        
        completed = dict_.get("completed")
        if completed != "All":
            filters.append(Task.completed == (completed == "Completed"))
            
        start_date_min = dict_.get("start_date_min")
        start_date_max = dict_.get("start_date_max")
        end_date_min = dict_.get("end_date_min")
        end_date_max = dict_.get("end_date_max")
        
        if start_date_min:
            filters.append(Task.start_date >= datetime.datetime.fromisoformat(start_date_min))
        if start_date_max:
            filters.append(Task.start_date <= datetime.datetime.fromisoformat(start_date_max))
        if end_date_min:
            filters.append(Task.end_date >= datetime.datetime.fromisoformat(end_date_min))
        if end_date_max:
            filters.append(Task.end_date <= datetime.datetime.fromisoformat(end_date_max))  
              
        query = DB.session.query(Task).filter(and_(*filters))
        websocket.emit('task_data', list(map(lambda task: task.to_dict(), query.all())), room=str(dict_.get("user_id")))
    