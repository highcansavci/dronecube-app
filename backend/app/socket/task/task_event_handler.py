from run import APP
from app.socket.handler.dronecube_handler import DronecubeHandler
    
@DronecubeHandler.on("filter_tasks")
def filter_all_tasks(self, data):
    with APP.app_context():
        return APP.task_controller.filter_all_tasks_socket(data, self)