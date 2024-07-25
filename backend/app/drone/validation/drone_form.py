from wtforms import Form, StringField, FloatField, validators
from wtforms.validators import DataRequired, NumberRange
from app.util.validation.float_converter import ConvertToFloat


class DroneForm(Form):
    name = StringField("name", validators=[DataRequired()])
    latitude = FloatField("latitude", validators=[DataRequired(), ConvertToFloat(), NumberRange(min=-90, max=90)])
    longitude = FloatField("longitude", validators=[DataRequired(), ConvertToFloat(), NumberRange(min=-180, max=180)])
    altitude = FloatField("altitude", validators=[DataRequired(), ConvertToFloat()])
    home_latitude = FloatField("home_latitude", validators=[DataRequired(), ConvertToFloat(), NumberRange(min=-90, max=90)])
    home_longitude = FloatField("home_longitude", validators=[DataRequired(), ConvertToFloat(), NumberRange(min=-180, max=180)])
    home_altitude = FloatField("home_altitude", validators=[DataRequired(), ConvertToFloat()])
    velocity_x = FloatField("velocity_x", validators=[DataRequired(), ConvertToFloat()])
    velocity_y = FloatField("velocity_y", validators=[DataRequired(), ConvertToFloat()])
    velocity_z = FloatField("velocity_z", validators=[DataRequired(), ConvertToFloat()])
    connected = StringField("connected", validators=[DataRequired(), validators.Regexp(r'(Connected|Not Connected)')])