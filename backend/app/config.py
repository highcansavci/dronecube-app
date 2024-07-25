from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://dronecube:dronecubeapp@localhost:5432/dronecubedb"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    RESET_PASS_TOKEN_MAX_AGE = 10000
    MAIL_SERVER = 'smtp.gmail.com'
    REMEMBER_COOKIE_DURATION = timedelta(days=1)
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    SESSION_COOKIE_SECURE = True
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = True
    REMEMBER_COOKIE_HTTPONLY = True
    SESSION_TYPE = 'redis'
    SESSION_COOKIE_NAME = "dronecookie"
    MAIL_USERNAME = 'drone.cube.reset@gmail.com'
    MAIL_PASSWORD = 'oqikhksxfryfjmfq'
    UPLOAD_FOLDER = "uploads"
    MINIO_ENDPOINT = 'localhost:9000'
    MINIO_ACCESS_KEY = 'minio_access_key'
    MINIO_SECRET_KEY = 'minio_secret_key'
    MINIO_BUCKET = 'dronecube'
    UTC = 3
    SECRET_KEY_NBYTES = 16
    IMAGE_WIDTH = 512
    IMAGE_HEIGHT = 512
    IMAGE_CHANNEL = 3
    NUM_IMAGES = 5