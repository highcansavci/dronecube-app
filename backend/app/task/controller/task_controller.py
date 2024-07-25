from flask import jsonify
from app.task.validation.task_form import TaskForm


class TaskController:
    # Singleton Controller
    _instance = None
    
    def __init__(self, task_service) -> None:
        self.task_service = task_service
        
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(TaskController, cls).__new__(cls)
            cls._instance.__initialize(*args, **kwargs)
        return cls._instance

    def __initialize(self, task_service):
        self.task_service = task_service
        
        
    def create_task(self, request):
        form = TaskForm(data=request.form)
        if form.validate():
            if form.assigned_drone_id.data:
                drone = self.task_service.query_drone(form.assigned_drone_id.data)
                if not drone:
                    return jsonify({'message': 'Drone is not found.'}), 404
                if not self.task_service.get_current_user() in drone.users:
                    return jsonify({'message': 'Drone is not belong to the user.'}), 400
                return self.task_service.create_task(form, drone)
            return self.task_service.create_task(form, None)
        return jsonify({'message': 'Bad request for creating the task.'}), 400

    def get_all_tasks(self, request):
        tasks = self.task_service.get_all_tasks()
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return self.task_service.serialize_all_tasks(tasks)
        return jsonify({'message': 'Invalid request header'}), 400

    def get_task(self, task_id, request):
        task = self.task_service.get_task(task_id)
        if request.headers.get("X-Requested-With") == "XMLHttpRequest":
            return self.task_service.serialize_task(task)
        return jsonify({'message': 'Invalid request header'}), 400

    def update_task(self, task_id, request):
        task = self.task_service.get_task(task_id)
        return self.task_service.update_task(request.form, task)

    def delete_task(self, task_id):
        task = self.task_service.get_task(task_id)
        self.task_service.delete_task(task)
        return jsonify({'message': 'Task is successfully deleted.'}), 200
    
    def execute_task(self, task_id):
        task = self.task_service.get_task(task_id)
        drone = self.task_service.query_drone(task.drone_id)
        if not drone.connected:
            return jsonify({'message': 'Task is not executed because the drone is not connected. Please connect the drone before executing the task.'}), 400
        self.task_service.execute_task(task, task_id)
        return jsonify({'message': 'Task execution is successful.'}), 200
    
    def filter_all_tasks_socket(self, data, websocket):
        self.task_service.filter_all_tasks_socket(data, websocket)