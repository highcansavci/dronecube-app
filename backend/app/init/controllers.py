from app.auth.controller.auth_controller import AuthController
from app.task.controller.task_controller import TaskController
from app.drone.controller.drone_controller import DroneController
from app.image.controller.image_controller import ImageController

def init_controller_container(app):
    with app.app_context():
        app.auth_controller = AuthController(app.auth_service)
        app.task_controller = TaskController(app.task_service)
        app.drone_controller = DroneController(app.drone_service)
        app.image_controller = ImageController(app.image_service, app.task_service)
        
        
        