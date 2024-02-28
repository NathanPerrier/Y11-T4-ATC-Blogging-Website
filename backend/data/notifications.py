from backend.config import *
from backend.db import *

class Notifications(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    
    #finish