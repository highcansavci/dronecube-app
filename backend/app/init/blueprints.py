from app.auth.router.auth_router import AUTH_BP
from app.task.router.task_router import TASK_BP
from app.drone.router.drone_router import DRONE_BP
from app.image.router.image_router import IMAGE_BP

def init_blueprints(app):
    with app.app_context():
        app.register_blueprint(AUTH_BP)
        app.register_blueprint(TASK_BP)
        app.register_blueprint(DRONE_BP)
        app.register_blueprint(IMAGE_BP)
        
        
        