from wtforms import FloatField, Form, StringField, DateTimeLocalField, validators
from wtforms.fields.numeric import IntegerField
from wtforms.validators import DataRequired, NumberRange, Optional
from app.util.validation.float_converter import ConvertToFloat


class TaskForm(Form):
    title = StringField("title", validators=[DataRequired()])
    start_date = DateTimeLocalField("start_date", validators=[DataRequired()])
    end_date = DateTimeLocalField("end_date", validators=[DataRequired()])
    completed = StringField("completed", validators=[DataRequired(), validators.Regexp(r'(Completed|Not Completed)')])
    assigned_drone_id = IntegerField("assigned_drone_id", validators=[Optional(), NumberRange(min=1)])
    latitude = FloatField("latitude", validators=[DataRequired(), ConvertToFloat(), NumberRange(min=-90, max=90)])
    longitude = FloatField("longitude", validators=[DataRequired(), ConvertToFloat(), NumberRange(min=-180, max=180)])
    altitude = FloatField("altitude", validators=[DataRequired(), ConvertToFloat()])