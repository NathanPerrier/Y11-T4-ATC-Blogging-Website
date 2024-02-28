from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class SignupForm(FlaskForm):
    name = StringField('name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    password = PasswordField('password', validators=[
        DataRequired(), 
        Length(min=8), 
        EqualTo('confirm_password', message='Passwords Must Match')
    ])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])
    submit = SubmitField('submit')