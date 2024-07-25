from minio import Minio
from app.config import Config

MINIO_CLIENT = Minio(Config.MINIO_ENDPOINT, access_key=Config.MINIO_ACCESS_KEY, secret_key=Config.MINIO_SECRET_KEY, secure=False)
def init_minio_client(app):
    app.minio_client = MINIO_CLIENT