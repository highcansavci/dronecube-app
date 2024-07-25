from urllib.parse import urljoin
from flask import render_template_string, session
from flask_login import current_user, login_user, logout_user
from flask_mailman import EmailMessage
from app.init.database import DB
from app.auth.model.user import User
from app.auth.service.auth_service import AuthService

RESET_PASSWORD_EMAIL_HTML_CONTENT = """
<p>Hello,</p>
<p>You are receiving this email because you requested a password reset for your account.</p>
<p>
    To reset your password
    <a href="{{ reset_password_url }}">click here</a>.
</p>
<p>
    Alternatively, you can paste the following link in your browser's address bar: <br>
    {{ reset_password_url }}
</p>
<p>If you have not requested a password reset please contact someone from the development team.</p>
<p>
    Thank you!
</p>
"""

class AuthServiceImpl(AuthService):
    # Singleton Service
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs)
        return cls._instance
    
    def loader_user(self, user_id):
        return DB.session.get(User, user_id)
    
    def query_user(self, email, username=None):
        query_ = DB.session.query(User).filter_by(email=email)
        if username is None:
            return query_.first()
        return query_.filter_by(username=username).first()
    
    def query_user_signup_email(self, email):
        return DB.session.query(User).filter_by(email=email).first()
    
    def query_user_signup_username(self, username):
        return DB.session.query(User).filter_by(username=username).first()
    
    def login_service_user(self, user, remember_me):
        return login_user(user, remember=remember_me)
    
    def create_user(self, username, email, password):
        user = User(username=username,
                    email=email,
                    password=password)
        DB.session.add(user)
        DB.session.commit()
        
    def is_user_authenticated(self):
        return current_user.is_authenticated   
        
    def send_reset_password_email(self, user):
        frontend_domain = "http://localhost:5173"
        reset_password_url = urljoin(frontend_domain, f"/reset-password/{user.generate_reset_password_token()}/{user.id}")
        email_body = render_template_string(RESET_PASSWORD_EMAIL_HTML_CONTENT, reset_password_url=reset_password_url)
        message = EmailMessage(
            subject="Reset Your Password",
            body=email_body,
            to=[user.email]
        )
        message.content_subtype = "html"
        message.send()
        
    def change_user_password(self, user, password):
        user.password = password
        DB.session.commit()

    def logout(self):
        session.user_id = None
        logout_user()

    def connect_to_socket(self, room, websocket):
        print("WebSocket opened")
        websocket.set_nodelay(True)
        websocket.emit("join_room", None)
    
    def disconnect_from_socket(self):
        print("WebSocket closed")
            
    def join_room(self, room, websocket):
        if room not in websocket.rooms:
            websocket.rooms[room] = []
        if websocket not in websocket.rooms[room]:    
            websocket.rooms[room].append(websocket)
            websocket.pubsub.subscribe(**{room: websocket.handle_redis_message})
            websocket.ioloop.add_callback(websocket.pubsub.run_in_thread)
            websocket.emit("filter_drones", None)
            websocket.emit("filter_tasks", None)
            print(f"Joined room: {room}")
    
    def leave_room(self, room, websocket):
        print(room, websocket.rooms)
        if room in websocket.rooms:
            websocket.rooms[room].remove(websocket)
            if not websocket.rooms[room]:  # If the room is empty, remove it
                del websocket.rooms[room]
        websocket.pubsub.unsubscribe(room)
        print(f"Left room: {room}")