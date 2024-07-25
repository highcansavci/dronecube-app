class AuthService:
    def loader_user(self, user_id):
        raise NotImplementedError
    
    def query_user(self, email, username):
        raise NotImplementedError
    
    def query_user_signup_email(self, email):
        raise NotImplementedError
    
    def query_user_signup_username(self, username):
        raise NotImplementedError
    
    def login_service_user(self, user):
        raise NotImplementedError
    
    def create_user(self, username, email, password):
        raise NotImplementedError
    
    def is_user_authenticated(self):
        raise NotImplementedError
    
    def send_reset_password_email(self, user):
        raise NotImplementedError
    
    def change_user_password(self, user, password):
        raise NotImplementedError
    
    def logout(self):
        raise NotImplementedError
    
    def connect_to_socketio(self):
        raise NotImplementedError
    
    def disconnect_from_socketio(self):
        raise NotImplementedError
    
    def join_room(self, id):
        raise NotImplementedError