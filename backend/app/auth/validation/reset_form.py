from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class ResetForm(FlaskForm):
    email = StringField("Email Address", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")
    