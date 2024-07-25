import secrets

SECRET_KEY = None
def init_secret_key(app, nbytes):
    SECRET_KEY = secrets.token_urlsafe(nbytes=nbytes)
    app.secret_key = SECRET_KEY
