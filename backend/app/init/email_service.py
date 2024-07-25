from flask_mailman import Mail

MAIL_CLIENT = Mail()
def init_mail_client(app):
    MAIL_CLIENT.init_app(app)