from flask import Blueprint, request
from app.init.login_manager import LOGIN_MANAGER
from flask import current_app as APP

AUTH_BP = Blueprint("auth", __name__)
        
@LOGIN_MANAGER.user_loader
def loader_user(user_id):
    print(user_id)
    return APP.auth_controller.loader_user(user_id)   
    
@AUTH_BP.route("/login-register", methods=["GET", "POST"])
def login_register():
    return APP.auth_controller.login_register(request)
    
@AUTH_BP.route("/reset-password", methods=["POST"])
def reset_password_request():
    return APP.auth_controller.reset_password_request(request)
    
@AUTH_BP.route("/reset-password/<token>/<int:user_id>", methods=["GET", "POST"])
def reset_password(token, user_id):
    return APP.auth_controller.reset_password(token, user_id)

@AUTH_BP.route('/csrf-token', methods=['GET'])
def get_csrf_token():
    return APP.auth_controller.get_csrf_token()

@AUTH_BP.route("/logout")
def logout():
    return APP.auth_controller.logout()
