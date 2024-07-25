from app.config import Config


def init_components(app):
    with app.app_context():
        from app.init.database import init_db
        from app.init.email_service import init_mail_client
        from app.init.login_manager import init_login_manager
        from app.init.minio_client import init_minio_client
        from app.init.secret_key import init_secret_key
        from app.init.cors import init_cors
        from app.init.csrf_protect import init_csrf_protect
        from app.init.services import init_service_container
        from app.init.controllers import init_controller_container
        from app.init.blueprints import init_blueprints
        from app.init.session import init_session

        init_service_container(app)
        init_controller_container(app)
        init_db(app)
        init_login_manager(app)
        init_mail_client(app)
        init_minio_client(app)
        init_secret_key(app, Config.SECRET_KEY_NBYTES)
        init_cors(app)
        init_csrf_protect(app)
        init_session(app)
        init_blueprints(app)

        import app.auth
        import app.drone
        import app.task
        import app.image