from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField, PasswordField, SubmitField, FileField
from wtforms.validators import DataRequired, Email, Length, EqualTo

class UpdateAccountForm(FlaskForm):
    first_name = StringField('first_name', validators=[DataRequired()])
    last_name = StringField('last_name', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
    username = StringField('username', validators=[DataRequired(), Length(min=2, max=40)])
    phone_number = StringField('phone_number', validators=[Length(max=10)])
    street_number = StringField('street_number', validators=[DataRequired()])
    street_name = StringField('street_name', validators=[DataRequired()])
    suburb = StringField('suburb', validators=[DataRequired()])
    postcode = StringField('postcode', validators=[DataRequired()])
    bio = StringField('bio', validators=[Length(max=300)])
    submit = SubmitField('submit')
    
class UpdatePasswordForm(FlaskForm):
    old_password = PasswordField('old_password', validators=[DataRequired(), Length(min=8, max=40)])
    new_password = PasswordField('new_password', validators=[
        DataRequired(), 
        Length(min=8), 
        EqualTo('confirm_password', message='Passwords must match')
    ])
    confirm_password = PasswordField('confirm_password', validators=[DataRequired()])
    submit = SubmitField('submit')
    
class UpdatePictureForm(FlaskForm):
    picture = FileField('picture')
    checkbox = BooleanField('checkbox')
    submit = SubmitField('submit')