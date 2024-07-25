import tornado.ioloop
import tornado.web
import tornado.websocket
import json
import redis
import socket
from run import APP

class DronecubeHandler(tornado.websocket.WebSocketHandler):
    event_handlers = {}
    rooms = {}
    try:
        pool = redis.ConnectionPool(
            host='localhost',
            port=6379,
            db=0,
            socket_timeout=10,
            socket_keepalive=True,
            socket_keepalive_options={
                socket.TCP_KEEPIDLE: 300,
                socket.TCP_KEEPINTVL: 60,
                socket.TCP_KEEPCNT: 5
            }
        )
        redis_client = redis.Redis(connection_pool=pool)
        redis_client.ping()  # Check connection
        print("Connected to Redis successfully!")
    except redis.exceptions.ConnectionError as e:
        print(f"Redis connection error: {e}")
    pubsub = redis_client.pubsub()
    ioloop = tornado.ioloop.IOLoop.current()

    def on_message(self, message):
        message = json.loads(message)
        event = message.get('event')
        data = message.get('data')

        if event in self.event_handlers:
            handler = self.event_handlers[event]
            handler(self, data)
        else:
            print(f"No handler for event: {event}")

    def send_to_room(self, room, event, data):
        message = json.dumps({'event': event, 'data': data})
        self.redis_client.publish(room, message)
        print(f"Sent message to room {room}: {message}")

    def handle_redis_message(self, message):
        if message['type'] == 'message':
            room = message['channel'].decode('utf-8')
            message_data = json.loads(message['data'].decode('utf-8'))
            event = message_data['event']
            data = message_data['data']
            for client in self.rooms.get(room, []):
                client.write_message(json.dumps({'event': event, 'data': data}))
        print(f"Received message: {message}")

    def check_origin(self, origin):
        return True

    def trigger_event(self, event, data):
        if event in self.event_handlers:
            handler = self.event_handlers[event]
            handler(self, data)

    @classmethod
    def on(cls, event_name):
        def decorator(func):
            cls.event_handlers[event_name] = func
            return func
        return decorator
    
    def emit(self, event, data, room=None):
        message = json.dumps({'event': event, 'data': data})
        if room:
            print(self.rooms)
            for client in self.rooms.get(room, []):
                if client.ws_connection is None or client.ws_connection.is_closing():
                    with APP.app_context():
                        APP.auth_controller.leave_room(room, client)
                else:
                    client.write_message(message)
            print(f"Sent message to room {room}: {message}")
        else:
            self.write_message(message)
            print(f"Sent message to client: {message}")
