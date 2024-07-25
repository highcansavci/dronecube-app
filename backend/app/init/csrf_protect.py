from flask_wtf import CSRFProtect

CSRF_PROTECT = CSRFProtect()
def init_csrf_protect(app):
    return CSRF_PROTECT.init_app(app)