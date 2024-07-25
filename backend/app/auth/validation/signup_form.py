from wtforms import Form, StringField, PasswordField, BooleanField, validators

class SignUpForm(Form):
    username = StringField('Username', [
        validators.DataRequired(message="Username is required")
    ])
    email = StringField('Email', [
        validators.DataRequired(message="Email is required"),
        validators.Email(message="A valid email is required")
    ])
    password = PasswordField('Password', [
        validators.DataRequired(message="Password is required"),
        validators.Length(min=10, message="Password must be at least 10 characters long"),
        validators.Regexp(r'(?=.*[A-Z])', message="Password must contain at least one uppercase letter"),
        validators.Regexp(r'(?=.*[a-z])', message="Password must contain at least one lowercase letter"),
        validators.Regexp(r'(?=.*[0-9])', message="Password must contain at least one number")
    ])
    remember_me = BooleanField('Remember Me')