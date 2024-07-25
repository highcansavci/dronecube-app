from flask import Flask
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    from app.init import init_components
    init_components(app)
    
    return app