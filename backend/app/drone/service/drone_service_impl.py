import json
import math
import threading
from flask_login import current_user
from sqlalchemy import func, and_, cast, Float
from app.init.database import DB
from app.auth.model.user import User
from app.drone.model.drone import Drone
from app.util.model.position import Position
from app.util.model.velocity import Velocity
from app.drone.service.drone_service import DroneService
from app.util.distance.latitude_longitude_distance import distance_between_points
from app.util.distance.altitude_distance import altitude_difference
from app.util.distance.slerp import slerp
import time
from flask import current_app

class DroneServiceImpl(DroneService):
    # Singleton Service
    _instance = None
    _locks = {}
    _threads = {}
        
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DroneServiceImpl, cls).__new__(cls)
        return cls._instance
    
    def get_current_user(self):
        return DB.session.get(User, current_user.id)
    
    def serialize_drones(self, drones):
        return json.dumps(Drone.serialize_list(drones.all()))
    
    def serialize_drone(self, drone):
        return json.dumps(Drone.serialize(drone))
    
    def create_drone(self, user, form):
        global_position = Position(float(form.latitude.data), float(form.longitude.data), float(form.altitude.data))
        home_position = Position(float(form.home_latitude.data), float(form.home_longitude.data), float(form.home_altitude.data))
        velocity = Velocity(float(form.velocity_x.data), float(form.velocity_y.data), float(form.velocity_z.data))
        drone = Drone(name=form.name.data,
                      global_position=global_position,
                      home_position=home_position,
                      velocity=velocity,
                      connected=bool(form.connected.data == "Connected"),
                      assigned_tasks=list(),
                      executing_tasks=list())
        user.drones.append(drone)
        DB.session.add(drone)
        DB.session.commit()
        self._locks[drone.id] = threading.Lock()
        self._threads[drone.id] = None
        return self.serialize_drone(drone)
    
    def create_drone_socket(self, dict_, websocket):
        global_position = Position(float(dict_["latitude"]), float(dict_["longitude"]), float(dict_["altitude"]))
        home_position = Position(float(dict_["home_latitude"]), float(dict_["home_longitude"]), float(dict_["home_altitude"]))
        velocity = Velocity(float(dict_["velocity_x"]), float(dict_["velocity_y"]), float(dict_["velocity_z"]))
        drone = Drone(name=dict_["name"],
                      global_position=global_position,
                      home_position=home_position,
                      velocity=velocity,
                      connected=bool(dict_["connected"] == "Connected"),
                      assigned_tasks=list(),
                      executing_tasks=list())
        user = current_app.auth_controller.loader_user(dict_["user_id"])
        user.drones.append(drone)
        DB.session.add(drone)
        DB.session.commit()
        self._locks[drone.id] = threading.Lock()
        self._threads[drone.id] = None
        websocket.emit("drone_created", drone.to_dict(), room=str(dict_["user_id"]))
        
    def query_drone(self, drone_id):
        return DB.session.query(Drone).filter_by(id=drone_id).first()
    
    def query_task(self, task_id):
        return self.task_service.get_task(task_id)
    
    def broadcast_drone_information(self, drone, user_id, websocket):
        websocket.emit("drone_data_response", drone.to_dict(), room=str(user_id))
        
    def filter_all_drones(self, drones, form):
        filters = []
        name = form.get("name")
        if name:
            filters.append(Drone.name == name)
        
        filter_fields = {
            'latitude': ('global_position', 1),
            'longitude': ('global_position', 2),
            'altitude': ('global_position', 3),
            'home_latitude': ('home_position', 1),
            'home_longitude': ('home_position', 2),
            'home_altitude': ('home_position', 3),
            'velocity_x': ('velocity', 1),
            'velocity_y': ('velocity', 2),
            'velocity_z': ('velocity', 3)
        }
        
        for field, (column_name, part) in filter_fields.items():
            min_value = float(form.get(f"{field}_min", math.nan))
            max_value = float(form.get(f"{field}_max", math.nan))
            
            if not math.isnan(min_value):
                filters.append(cast(func.split_part(getattr(Drone, column_name), ',', part), Float) >= min_value)
            if not math.isnan(max_value):
                filters.append(cast(func.split_part(getattr(Drone, column_name), ',', part), Float) <= max_value)
        
        connected = form.get("connected")
        if connected != "All":
            filters.append(Drone.connected == (connected == "Connected"))
        query = DB.session.query(Drone).filter(and_(*filters))
        return self.serialize_drones(query)
    
    def filter_all_drones_socket(self, dict_, websocket):
        filters = []
        name = dict_.get("name")
        if name:
            filters.append(Drone.name == name)
        
        filter_fields = {
            'latitude': ('global_position', 1),
            'longitude': ('global_position', 2),
            'altitude': ('global_position', 3),
            'home_latitude': ('home_position', 1),
            'home_longitude': ('home_position', 2),
            'home_altitude': ('home_position', 3),
            'velocity_x': ('velocity', 1),
            'velocity_y': ('velocity', 2),
            'velocity_z': ('velocity', 3)
        }
        
        for field, (column_name, part) in filter_fields.items():
            min_value = float(dict_.get(f"{field}_min", math.nan))
            max_value = float(dict_.get(f"{field}_max", math.nan))
            
            if not math.isnan(min_value):
                filters.append(cast(func.split_part(getattr(Drone, column_name), ',', part), Float) >= min_value)
            if not math.isnan(max_value):
                filters.append(cast(func.split_part(getattr(Drone, column_name), ',', part), Float) <= max_value)
        
        connected = dict_.get("connected")
        if connected != "All":
            filters.append(Drone.connected == (connected == "Connected"))
        query = DB.session.query(Drone).filter(and_(*filters))
        websocket.emit('drone_data', list(map(lambda drone: drone.to_dict(), query.all())), room=str(dict_.get("user_id")))

    def update_drone(self, drone, data):
        drone.name = drone.name if data.get("name") == "" else data.get("name")
        latitude = drone.global_position.latitude if data.get("latitude") == "null" else data.get("latitude")
        longitude = drone.global_position.longitude if data.get("longitude") == "null" else data.get("longitude")
        altitude = drone.global_position.altitude if data.get("altitude") == "null" else data.get("altitude")
        global_position = Position(latitude, longitude, altitude)
        drone.global_position = global_position
        home_latitude = drone.home_position.latitude if data.get("home_latitude") == "null" else data.get("home_latitude")
        home_longitude = drone.home_position.longitude if data.get("home_longitude") == "null" else data.get("home_longitude")
        home_altitude = drone.home_position.altitude if data.get("home_altitude") == "null" else data.get("home_altitude")
        home_position = Position(home_latitude, home_longitude, home_altitude)
        drone.home_position = home_position
        velocity_x = drone.velocity.velocity_x if data.get("velocity_x") == "null" else data.get("velocity_x")
        velocity_y = drone.velocity.velocity_y if data.get("velocity_y") == "null" else data.get("velocity_y")
        velocity_z = drone.velocity.velocity_z if data.get("velocity_z") == "null" else data.get("velocity_z")
        velocity = Velocity(velocity_x, velocity_y, velocity_z)
        drone.velocity = velocity
        drone.connected = drone.connected if data.get("connected") == "null" else data.get("connected") == "Connected"
        DB.session.commit()
        
    def delete_drone(self, drone):
        DB.session.delete(drone)
        DB.session.commit()
        if self._locks.get(drone.id):
            del self._locks[drone.id]
        if self._threads.get(drone.id):
            self._threads[drone.id].join()
            del self._threads[drone.id]
    
    def connect_drone(self, drone_id, user_id, websocket):
        from run import APP
        with APP.app_context():
            drone = self.query_drone(drone_id)
            drone.connected = not drone.connected
            DB.session.commit()
            websocket.emit("update_drone_status", drone.to_dict(), room=str(user_id))
        
    def assign_task_to_drone(self, drone, task):
        if self._locks.get(drone.id) is None:
            self._locks[drone.id] = threading.Lock()
        with self._locks.get(drone.id):
            drone.assigned_tasks.append(task)
            task.assigned_drone_id = drone.id
        DB.session.commit()
        
    def add_task_to_execution(self, drone, task):
        if self._locks.get(drone.id) is None:
            self._locks[drone.id] = threading.Lock()
        with self._locks.get(drone.id):
            if task not in drone.executing_tasks:
                drone.executing_tasks.append(task)
                task.executing_drone_id = drone.id
        DB.session.commit()
        
    def start_task_execution(self, drone_id, websocket):
        drone = self.query_drone(drone_id)
        if self._locks.get(drone.id) is None:
            self._locks[drone.id] = threading.Lock()
        with self._locks.get(drone.id):
            if not self._threads[drone.id] and drone.executing_tasks:
                thread = threading.Thread(target=self._execute_tasks, args=(drone, websocket))
                self._threads[drone.id] = thread
                thread.start()
    
    def _execute_tasks(self, drone, websocket):
        while drone.connected and drone.executing_tasks:
            if self._locks.get(drone.id) is None:
                self._locks[drone.id] = threading.Lock()
            with self._locks.get(drone.id):
                task = drone.executing_tasks[0]
            if task.completed:
                with self._locks[drone.id]:
                    drone.executing_tasks.pop(0)
                continue
            self.execute_task(drone, task, websocket)
            with self._locks.get(drone.id):
                drone.executing_tasks.pop(0)
        self._threads[drone.id] = None
    
    def execute_task(self, drone, task, websocket):
        if drone.connected and task in drone.executing_tasks:
            self.update_drone_location(drone, task.task_position, websocket)
            current_app.task_service.execute_task(task, task.id)
            current_app.task_service.complete_task(task)
            websocket.emit('task_completed', {'drone_id': drone.id, 'task_id': task.id}, room=str(current_user.id))

    def update_drone_location(self, drone, task_position, websocket):
        current_position = drone.global_position
        velocity = drone.velocity
        distance_xy = distance_between_points(current_position.latitude, current_position.longitude, task_position.latitude, task_position.longitude)
        distance_z = altitude_difference(current_position.altitude, task_position.altitude)
        combined_velocity_xy = math.sqrt(velocity.velocity_x ** 2 + velocity.velocity_y ** 2)
        if combined_velocity_xy != 0:
            time_to_reach_xy = abs(distance_xy / combined_velocity_xy)
        else:
            time_to_reach_xy = float('inf') if distance_xy != 0 else 0
        if velocity.velocity_z != 0:
            time_to_reach_z = abs(distance_z / velocity.velocity_z)
        else:
            time_to_reach_z = float('inf') if distance_z != 0 else 0
        time_to_reach = max(time_to_reach_xy, time_to_reach_z)
        tick_interval = 0.1 
        ticks = int(time_to_reach / tick_interval) if time_to_reach > 0 else 0
        for tick in range(ticks + 1):
            progress = tick / ticks if ticks > 0 else 1.0
            new_latitude, new_longitude = slerp(current_position.latitude, current_position.longitude, task_position.latitude, task_position.longitude, progress)
            new_altitude = current_position.altitude + progress * distance_z
            new_altitude = current_position.altitude + (task_position.altitude - current_position.altitude) * progress
            drone.global_position = Position(new_latitude, new_longitude, new_altitude)
            websocket.emit('drone_position_updated', {'drone_id': drone.id, 'latitude': drone.global_position.latitude, 'longitude': drone.global_position.longitude, 'altitude': drone.global_position.altitude}, room=str(current_user.id))            
            time.sleep(tick_interval)        
        DB.session.commit()
    
    def cancel_task_execution(self, drone, task):
        if self._locks.get(drone.id) is None:
                self._locks[drone.id] = threading.Lock()
        with self._locks.get(drone.id):
            if task in drone.executing_tasks:
                drone.executing_tasks.remove(task)
                task.executing_drone_id = None
        DB.session.commit()
        
    def cancel_task_assignment(self, drone, task):
        if self._locks.get(drone.id) is None:
            self._locks[drone.id] = threading.Lock()
        with self._locks.get(drone.id):
            if task in drone.executing_tasks:
                drone.executing_tasks.remove(task)
                task.executing_drone_id = None
            if task in drone.assigned_tasks:
                drone.assigned_tasks.remove(task)
                task.assigned_drone_id = None
        DB.session.commit()
    
    def bulk_assign_tasks_to_drone(self, drone_id, task_ids):
        drone = self.query_drone(drone_id)
        if self._locks.get(drone.id) is None:
            self._locks[drone.id] = threading.Lock()
        with self._locks.get(drone.id):
            for task_id in task_ids:
                task = self.query_task(task_id)
                drone.assigned_tasks.append(task)
                task.assigned_drone_id = drone.id
        DB.session.commit()
        return self.serialize_drone(drone)

    def bulk_add_tasks_to_execution(self, drone_id, task_ids):
        drone = self.query_drone(drone_id)
        if self._locks.get(drone.id) is None:
            self._locks[drone.id] = threading.Lock()
        with self._locks.get(drone.id):
            for task_id in task_ids:
                task = self.query_task(task_id)
                if task not in drone.executing_tasks:
                    drone.executing_tasks.append(task)
                    task.executing_drone_id = drone.id
        DB.session.commit()
        if drone.connected:
            self.start_task_execution(drone.id)
        return self.serialize_drone(drone)
    
    def bulk_cancel_task_execution(self, drone_id, task_ids):
        drone = self.query_drone(drone_id)
        if self._locks.get(drone.id) is None:
            self._locks[drone.id] = threading.Lock()
        with self._locks.get(drone.id):
            for task_id in task_ids:
                task = self.query_task(task_id)
                if task in drone.executing_tasks:
                    drone.executing_tasks.remove(task)
                    task.executing_drone_id = None
        DB.session.commit()
        return self.serialize_drone(drone)

    def bulk_cancel_task_assignment(self, drone_id, task_ids):
        drone = self.query_drone(drone_id)
        if self._locks.get(drone.id) is None:
            self._locks[drone.id] = threading.Lock()
        with self._locks.get(drone.id):
            for task_id in task_ids:
                task = self.query_task(task_id)
                if task in drone.executing_tasks:
                    drone.executing_tasks.remove(task)
                    task.executing_drone_id = None
                if task in drone.assigned_tasks:
                    drone.assigned_tasks.remove(task)
                    task.assigned_drone_id = None
        DB.session.commit()
        return self.serialize_drone(drone)