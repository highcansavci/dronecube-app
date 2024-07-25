import tornado.ioloop
import tornado.web
import tornado.websocket
from app.socket.handler.dronecube_handler import DronecubeHandler
import app.socket.auth.auth_event_handler 
import app.socket.drone.drone_event_handler
import app.socket.task.task_event_handler

        
def make_app():
    return tornado.web.Application([
        (r"/websocket", DronecubeHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    print("WebSocket server started at ws://localhost:8888/websocket")
    tornado.ioloop.IOLoop.current().start()
