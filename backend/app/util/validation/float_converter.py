from wtforms import validators

class ConvertToFloat:
    def __call__(self, form, field):
        try:
            field.data = float(field.data)
        except ValueError:
            raise validators.ValidationError("Invalid number")