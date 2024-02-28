from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class LoginForm(FlaskForm):
    email = StringField('email', validators=[DataRequired()]) #Email()
    password = PasswordField('password', validators=[DataRequired(), Length(min=8)])
    submit = SubmitField('submit')