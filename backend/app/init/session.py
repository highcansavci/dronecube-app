from flask_session import Session

SESSION = Session()
def init_session(app):
    SESSION.init_app(app)