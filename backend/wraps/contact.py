from backend.forms.email import Email
from functools import wraps
from flask import request

def handle_contact_request(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        if request.method == 'POST':
            data = request.get_json()
            Email().send_contact_us_emails(data['name'], data['email'], data['subject'], data['message'])
        return route_func(*args, **kwargs)
    return wrapper

    