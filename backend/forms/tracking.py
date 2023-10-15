from datetime import datetime as dt

from wtforms.validators import DataRequired
from wtforms import fields
from wtforms_sqlalchemy.fields import QuerySelectField

from backend.tracking.models import Site

from backend.config import *

class SiteForm(FlaskForm):
    base_url = fields.StringField(validators=[DataRequired()])


class VisitForm(FlaskForm):
    browser = fields.StringField()
    date = fields.DateField(default=dt.now)
    event = fields.StringField()
    url = fields.StringField(validators=[DataRequired()])
    ip_address = fields.StringField()
    location = fields.StringField()
    latitude = fields.StringField()
    longitude = fields.StringField()
    site = QuerySelectField(validators=[DataRequired()], query_factory=lambda: Site.query.all())