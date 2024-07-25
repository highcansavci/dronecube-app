from flask_sqlalchemy import SQLAlchemy

DB = SQLAlchemy()

def init_db(app):
    DB.init_app(app)
    with app.app_context():
        DB.create_all()