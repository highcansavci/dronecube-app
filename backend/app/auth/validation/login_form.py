from flask_wtf import FlaskForm
from wtforms import BooleanField, PasswordField, StringField, SubmitField
from wtforms.validators import DataRequired, Email

class LoginForm(FlaskForm):
    username = StringField('Username', [
        DataRequired(message="Username is required")
    ])
    email = StringField('Email', [
        DataRequired(message="Email is required"),
        Email(message="A valid email is required")
    ])
    password = PasswordField('Password', [
        DataRequired(message="Password is required"),
    ])
    remember_me = BooleanField('Remember Me')
    