from flask import render_template, session
from functools import wraps

def confirmed_page_access(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        if session.pop('confirmed_access_confirmed', None):
            return render_template('password_confirmed.html')
        return route_func(*args, **kwargs)
    return wrapper