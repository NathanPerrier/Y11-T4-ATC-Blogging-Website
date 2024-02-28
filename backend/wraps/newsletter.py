from backend.forms.__init__ import create_email, send_email 
from backend.authentication.user import User
from backend.data.newsletter import Newsletter
from backend.forms.email import Email
from backend.db import db
from backend.config import *
from functools import wraps
from flask import request

def handle_newsletter(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            email=request.form.get('email')
            success, error = Newsletter().add_user_to_newsletter(db, email)
            if success: send_email('contact.webgenieai@gmail.com', email, create_email('Subscriber', email, 'Thank You For Joining Our Newsletter!', 'Thank you for joining our newsletter, we will keep you updated with the latest news and updates!'))
            return jsonify(success=success, error=error)
        return route_func(*args, **kwargs)
    return wrapper

    