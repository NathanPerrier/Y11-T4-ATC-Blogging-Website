from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class ChangePasswordForm(FlaskForm):
    email = StringField('email', validators=[DataRequired(), Email()])
    code = PasswordField('code', validators=[DataRequired(), Length(min=6, max=6)])
    new_password = PasswordField('new password', validators=[
        DataRequired(), 
        Length(min=8), 
        EqualTo('confirm_password', message='Passwords Must Match')
    ])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])
    submit = SubmitField('submit')
    
    
# redundant!! 