import dataclasses
from flask_login import UserMixin
from itsdangerous import URLSafeTimedSerializer, BadSignature, SignatureExpired
from app.config import Config
from app.init.database import DB
from app.init.secret_key import SECRET_KEY

@dataclasses.dataclass
class User(UserMixin, DB.Model):
    __tablename__ = 'users'

    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(250), unique=True, nullable=False)
    email = DB.Column(DB.String(50), unique=True, nullable=False)
    password = DB.Column(DB.String(250), nullable=False)
    drones = DB.relationship('Drone', secondary="user_drones", lazy="dynamic", back_populates='users')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def generate_reset_password_token(self):
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        return serializer.dumps(self.email, salt=self.password)

    @staticmethod
    def validate_reset_password_token(token: str, user_id: int):
        user = DB.session.get(User, user_id)
        if user is None:
            return None
        serializer = URLSafeTimedSerializer(SECRET_KEY)
        try:
            token_user_email = serializer.loads(
                token,
                max_age=Config.RESET_PASS_TOKEN_MAX_AGE,
                salt=user.password
            )
        except (BadSignature, SignatureExpired):
            return None
        if token_user_email != user.email:
            return None
        return user

