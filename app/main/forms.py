from flask_wtf import FlaskForm
from wtforms import TextField, TextAreaField, StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    email = TextField('email:', validators=[DataRequired()])
    password = PasswordField('password:', validators=[DataRequired()])
