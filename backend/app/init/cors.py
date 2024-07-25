from flask_cors import CORS

CORS_ = CORS(supports_credentials=True, resources={r"/*": {"origins": "*"}})
def init_cors(app):
    CORS_.init_app(app)