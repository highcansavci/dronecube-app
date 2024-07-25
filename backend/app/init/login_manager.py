from flask_login import LoginManager

LOGIN_MANAGER = LoginManager()
def init_login_manager(app):
    LOGIN_MANAGER.init_app(app)
