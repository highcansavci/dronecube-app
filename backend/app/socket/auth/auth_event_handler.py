from run import APP
from app.socket.handler.dronecube_handler import DronecubeHandler
    
@DronecubeHandler.on("connect")
def connect_to_socketio(self, data):
    with APP.app_context():
        return APP.auth_controller.connect_to_socket(data, self)

@DronecubeHandler.on("disconnect")
def disconnect_from_socketio(self, data):
    with APP.app_context():
        return APP.auth_controller.disconnect_from_socket()

@DronecubeHandler.on("join_room")
def join_room(self, data):
    with APP.app_context():
        return APP.auth_controller.join_room(data.get("room"), self)

@DronecubeHandler.on("leave_room")
def leave_room(self, data):
    with APP.app_context():
        return APP.auth_controller.leave_room(data.get("room"), self)
