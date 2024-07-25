from flask_wtf import FlaskForm
from wtforms.fields.simple import PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, EqualTo

class PasswordForm(FlaskForm):
    new_password = PasswordField(validators=[DataRequired(), Length(min=10, max=80)])
    repeat_password = PasswordField(validators=[DataRequired(), EqualTo("new_password")])
    submit = SubmitField("Reset Password")
    