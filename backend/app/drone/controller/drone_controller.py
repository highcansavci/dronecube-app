from flask import current_app, jsonify
from app.drone.validation.drone_form import DroneForm


class DroneController:
    # Singleton Controller
    _instance = None
    
    def __init__(self, drone_service) -> None:
        self.drone_service = drone_service

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(DroneController, cls).__new__(cls)
            cls._instance.__initialize(*args, **kwargs)
        return cls._instance

    def __initialize(self, drone_service):
        self.drone_service = drone_service
    
    def get_all_drones(self, request):
        user = self.drone_service.get_current_user()
        if user:
            drones = user.drones
            if request.headers.get("X-Requested-With") == "XMLHttpRequest":
                return self.drone_service.serialize_drones(drones), 200
            return jsonify({'message': 'Invalid request header'}), 400
        return jsonify({"message": "User is not found."}), 404
    
    def filter_all_drones(self, request):
        user = self.drone_service.get_current_user()
        if user:
            drones = user.drones
            form = request.form
            return self.drone_service.filter_all_drones(drones, form), 200
        return jsonify({"message": "User is not found."}), 404
    
    def filter_all_drones_socket(self, dict_, websocket):
        self.drone_service.filter_all_drones_socket(dict_, websocket)
        
    def create_drone(self, request):
        form = DroneForm(data=request.form)
        if form.validate():
            user = self.drone_service.get_current_user()
            if user:
                return self.drone_service.create_drone(user, form), 201
            return jsonify({"message": "User is not found."}), 404
        return jsonify({"message": "Bad request for creating the drone."}), 400
    
    def create_drone_socket(self, dict_, websocket):
        self.drone_service.create_drone_socket(dict_, websocket)
            
    def get_drone(self, drone_id):
        drone = self.drone_service.query_drone(drone_id)
        user = self.drone_service.get_current_user()
        if drone in user.drones:
            return self.drone_service.serialize_drone(drone), 200
        return jsonify({'message': 'Drone does not belong to the current user.'}), 404
    
    def get_drone_socket(self, drone_id, user_id, websocket):
        drone = self.drone_service.query_drone(drone_id)
        user = current_app.auth_controller.loader_user(user_id)
        if drone in user.drones:
            self.drone_service.broadcast_drone_information(drone, user_id, websocket)
    
    def update_drone(self, drone_id, request):
        drone = self.drone_service.query_drone(drone_id)
        if self.drone_service.get_current_user() in drone.users:
            self.drone_service.update_drone(drone, request.form)
            return self.drone_service.serialize_drone(drone), 200
        return jsonify({'message': 'Drone does not belong to the current user.'}), 404

    def delete_drone(self, drone_id):
        drone = self.drone_service.query_drone(drone_id)
        if self.drone_service.get_current_user() in drone.users:
            self.drone_service.delete_drone(drone)
            return jsonify({'message': 'Drone is deleted successfully'}), 200
        return jsonify({'message': 'Drone is not belong to the current user.'}), 404
    
    def connect_drone(self, drone_id, user_id, websocket):
        self.drone_service.connect_drone(drone_id, user_id, websocket)
    
    def assign_task_to_drone(self, drone_id, task_id):
        drone = self.drone_service.query_drone(drone_id)
        task = self.drone_service.query_task(task_id)
        if not drone:
            return jsonify({'message': "Drone not found"}), 404
        if not task:
            return jsonify({'message': "Task not found"}), 404
        if task.completed:
            return jsonify({'message': "Task is already completed"}), 400
        if task in drone.assigned_tasks:
            return jsonify({'message': "Task is already assigned to this drone"}), 400
        self.drone_service.assign_task_to_drone(self, drone, task)
        return jsonify({'message': "Task assigned to drone successfully"}), 200 
    
    def start_executing_task(self, drone_id, task_id):
        drone = self.drone_service.query_drone(drone_id)
        task = self.drone_service.query_task(task_id)
        if not drone:
            return jsonify({'message': "Drone not found"}), 404
        if not task:
            return jsonify({'message': "Task not found"}), 404
        if task.completed:
            return jsonify({'message': "Task is already completed"}), 400
        if task not in drone.assigned_tasks:
            return jsonify({'message': "Task is not assigned to the drone"}), 400
        if task in drone.executing_tasks:
            return jsonify({'message': "Task is already being executed by this drone"}), 400
        self.drone_service.start_executing_task(drone, task)
        return jsonify({'message': "Drone started executing task successfully"}), 200
    
    def start_executing_task(self, drone_id, task_id, websocket):
        drone = self.drone_service.query_drone(drone_id)
        task = self.drone_service.query_task(task_id)
        if not drone:
            websocket.emit("drone_not_found", "Drone not found")
            return
        if not task:
            websocket.emit("task_not_found", "Task not found")
            return
        if task.completed:
            websocket.emit("task_already_completed", "Task is already completed")
            return
        if task not in drone.assigned_tasks:
            websocket.emit("task_not_assigned", "Task is not assigned to the drone")
            return
        if task not in drone.executing_tasks:
            websocket.emit("task_not_executed", "Task is not configured to execute for the drone")
            return
        self.drone_service.start_executing_task(drone, task, websocket)
    
    def cancel_task_execution(self, drone_id, task_id):
        drone = self.drone_service.query_drone(drone_id)
        task = self.drone_service.query_task(task_id)
        if not drone:
            return jsonify({'message': "Drone not found"}), 404
        if not task:
            return jsonify({'message': "Task not found"}), 404
        if task.completed:
            return jsonify({'message': "Task is already completed"}), 400
        if task not in drone.assigned_tasks:
            return jsonify({'message': "Task is not assigned to the drone"}), 400
        if task not in drone.executing_tasks:
            return jsonify({'message': "Execution of this task is canceled"}), 400
        self.drone_service.cancel_task_execution(drone, task)
        return jsonify({'message': "Drone started executing task successfully"}), 200
    
    def cancel_task_assignment(self, drone_id, task_id):
        drone = self.drone_service.query_drone(drone_id)
        task = self.drone_service.query_task(task_id)
        if not drone:
            return jsonify({'message': "Drone not found"}), 404
        if not task:
            return jsonify({'message': "Task not found"}), 404
        if task not in drone.assigned_tasks:
            return jsonify({'message': "Task is not assigned to the drone"}), 400
        self.drone_service.cancel_task_assignment(drone, task)
        return jsonify({'message': "Drone started executing task successfully"}), 200
    
    def bulk_assign_tasks_to_drone(self, drone_id, request):
        drone = self.drone_service.query_drone(drone_id)
        if not drone:
            return jsonify({'message': "Drone not found"}), 404
        task_ids = request.json.get('task_ids')
        if not task_ids:
            return jsonify({'message': "No task IDs provided"}), 400
        valid_task_ids = []
        for task_id in task_ids:
            task = self.drone_service.query_task(task_id)
            if not task:
                continue  
            if task.completed or task in drone.assigned_tasks:
                continue  
            valid_task_ids.append(task_id)
        if valid_task_ids.count() == 0:
            return jsonify({'message': "Task IDs are not valid"}), 400    
        self.drone_service.bulk_assign_tasks_to_drone(drone_id, valid_task_ids)
        return jsonify({'message': "Tasks assigned to drone successfully"}), 200

    def bulk_add_tasks_to_execution(self, drone_id, request):
        drone = self.drone_service.query_drone(drone_id)
        if not drone:
            return jsonify({'message': "Drone not found"}), 404
        task_ids = request.json.get('task_ids')
        if not task_ids:
            return jsonify({'message': "No task IDs provided"}), 400
        valid_task_ids = []
        for task_id in task_ids:
            task = self.drone_service.query_task(task_id)
            if not task:
                continue
            if task.completed:
                continue
            if task not in drone.assigned_tasks:
                continue
            if task in drone.executing_tasks:
                continue
            valid_task_ids.append(task_id)
        if valid_task_ids.count() == 0:
            return jsonify({'message': "Task IDs are not valid"}), 400 
        self.drone_service.bulk_add_tasks_to_execution(drone_id, valid_task_ids)
        return jsonify({'message': "Tasks added to execution successfully"}), 200

    def bulk_cancel_task_execution(self, drone_id, request):
        drone = self.drone_service.query_drone(drone_id)
        if not drone:
            return jsonify({'message': "Drone not found"}), 404
        task_ids = request.json.get('task_ids')
        if not task_ids:
            return jsonify({'message': "No task IDs provided"}), 400
        valid_task_ids = []
        for task_id in task_ids:
            task = self.drone_service.query_task(task_id)
            if not task:
                continue
            if task.completed:
                continue
            if task not in drone.assigned_tasks:
                continue
            if task not in drone.executing_tasks:
                continue
            valid_task_ids.append(task_id)
        if valid_task_ids.count() == 0:
            return jsonify({'message': "Task IDs are not valid"}), 400 
        self.drone_service.bulk_cancel_task_execution(drone_id, valid_task_ids)
        return jsonify({'message': "Task executions canceled successfully"}), 200

    def bulk_cancel_task_assignment(self, drone_id, request):
        drone = self.drone_service.query_drone(drone_id)
        if not drone:
            return jsonify({'message': "Drone not found"}), 404
        task_ids = request.json.get('task_ids')
        if not task_ids:
            return jsonify({'message': "No task IDs provided"}), 400
        valid_task_ids = []
        for task_id in task_ids:
            task = self.drone_service.query_task(task_id)
            if not task:
                continue
            if task.completed:
                continue
            if task not in drone.assigned_tasks:
                continue
            valid_task_ids.append(task_id)
        if valid_task_ids.count() == 0:
            return jsonify({'message': "Task IDs are not valid"}), 400     
        self.drone_service.bulk_cancel_task_assignment(drone_id, task_ids)
        return jsonify({'message': "Task assignments canceled successfully"}), 200