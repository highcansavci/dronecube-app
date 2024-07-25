from flask import jsonify, make_response
from flask_wtf.csrf import generate_csrf
from app.auth.model.user import User
from app.auth.validation.password_form import PasswordForm
from app.auth.validation.reset_form import ResetForm
from app.auth.service.auth_service_impl import AuthServiceImpl
from app.auth.validation.login_form import LoginForm
from app.auth.validation.signup_form import SignUpForm

class AuthController:
    # Singleton Controller
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AuthController, cls).__new__(cls)
            cls._instance.__initialize(*args, **kwargs)
        return cls._instance

    def __initialize(self, auth_service):
        self.auth_service = auth_service
    
    def __init__(self, auth_service: AuthServiceImpl) -> None:
        self.auth_service = auth_service
        
    def loader_user(self, user_id):
        return self.auth_service.loader_user(user_id)
    
    def get_csrf_token(self):
        csrf_token = generate_csrf()
        return jsonify({'csrf_token': csrf_token}), 200
    
    def login_register(self, request):
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        action = request.form.get("action")
        remember_me = request.form.get("remember_me")
        method = request.method
        if method == "POST" and action == "login":
            form = LoginForm(request.form)
            if not form.validate():
                errors = []
                for field, errs in form.errors.items():
                    errors.append(f"Error in the {getattr(form, field).label.text} field - {err}" for err in errs)
                return jsonify({'message': errors}), 400
            user = self.auth_service.query_user(username=username, email=email)
            if user is None:
                return jsonify({"message": "You are not registered. Please register on sign-up section."}), 404
            if user.password == request.form.get("password"):
                self.auth_service.login_service_user(user, remember_me)
                response = make_response(jsonify({"message": "You are successfully logged in."}))
                response.set_cookie("user_id", str(user.id),  httponly=False, secure=False, samesite='Lax', max_age=365 * 24 * 60 * 60)
                return response, 200
        elif method == "POST" and action == "sign-up":
            form = SignUpForm(request.form)
            if not form.validate():
                errors = []
                for field, errs in form.errors.items():
                    errors.append(f"Error in the {getattr(form, field).label.text} field - {err}" for err in errs)
                return jsonify({'message': errors}), 400
            user_email = self.auth_service.query_user_signup_email(email=email)
            if user_email is not None:
                return jsonify({"message": "The user account with the same email exists."}), 400
            user_username = self.auth_service.query_user_signup_username(username=username)
            if user_username is not None:
                return jsonify({"message": "The user account with the same username exists."}), 400 
            self.auth_service.create_user(username=username,
                                          email=email,
                                          password=password)
            return jsonify({"message": "You are successfully registered. You can log in."}), 201
        return jsonify({"message": "You have failed to register"}), 400
       
    
    def reset_password_request(self, request):
        email = request.form.get("email")
        if self.auth_service.is_user_authenticated():
            return jsonify({"message": "User is already authenticated."}), 302
        form = ResetForm()
        if form.validate_on_submit():
            user = self.auth_service.query_user(email=email)
            if user:
                self.auth_service.send_reset_password_email(user)
                return jsonify({"message": "Instructions to reset your password were sent to your email address."}), 303
            return jsonify({"message": "User with the specified email address is not found."}), 404    
        return jsonify({"message": "Bad request for resetting password."}), 400
    
    def reset_password(self, token, user_id):
        if self.auth_service.is_user_authenticated():
            return jsonify({"message": "User is already authenticated."}), 302
        user = User.validate_reset_password_token(token, user_id)
        if not user:
            return jsonify({"message": "Reset password is not successful, the user is not found or the token is expired."}), 404
        form = PasswordForm()
        if form.validate_on_submit():
            new_password = form.new_password.data
            if user.password == new_password:
                return jsonify({"message": "The new password should not be same as the old password."}), 400
            self.auth_service.change_user_password(user, new_password)
            return jsonify({"message": "Reset password is successful."}), 200
        return jsonify({"message": "Reset password is not successful, the password is not valid."}), 400

    def logout(self):
        self.auth_service.logout()
        return jsonify({"message": "User successfully logged out."}), 200
    
    def connect_to_socket(self, id, websocket):
        self.auth_service.connect_to_socket(id, websocket)
        
    def disconnect_from_socket(self):
        self.auth_service.disconnect_from_socket()    
        
    def join_room(self, id, websocket):
        self.auth_service.join_room(str(id), websocket)
        
    def leave_room(self, id, websocket):
        self.auth_service.leave_room(str(id), websocket)    
    
