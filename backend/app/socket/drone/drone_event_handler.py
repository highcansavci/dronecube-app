from run import APP
from app.socket.handler.dronecube_handler import DronecubeHandler

@DronecubeHandler.on("create_drone")
def create_drone(self, data):
    with APP.app_context():
        return APP.drone_controller.create_drone_socket(data, self)

@DronecubeHandler.on("request_drone_data")
def get_drone(self, data):
    with APP.app_context():
        return APP.drone_controller.get_drone_socket(data.get("id"), data.get("user_id"), self)

@DronecubeHandler.on("update_connection_status")
def connect_drone(self, data):
    with APP.app_context():
        return APP.drone_controller.connect_drone(data.get("id"), data.get("user_id"), self)
    
@DronecubeHandler.on("filter_drones")
def filter_all_drones(self, data):
    with APP.app_context():
        return APP.drone_controller.filter_all_drones_socket(data, self)
    
@DronecubeHandler.on("execute")
def start_executing_tasks(self, data):
    with APP.app_context():
        return APP.drone_controller.start_executing_task(data.get("drone_id"), data.get("task_id"), self)    