from app.auth.service.auth_service_impl import AuthServiceImpl
from app.task.service.task_service_impl import TaskServiceImpl
from app.drone.service.drone_service_impl import DroneServiceImpl
from app.image.service.image_service_impl import ImageServiceImpl

def init_service_container(app):
    with app.app_context():
        app.auth_service = AuthServiceImpl()
        app.task_service = TaskServiceImpl()
        app.drone_service = DroneServiceImpl()
        app.image_service = ImageServiceImpl()