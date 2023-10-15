from functools import wraps
from backend.authentication.user import User
from backend.config import *

def handle_login_request(route_func):
    @wraps(route_func)
    def wrapper(*args, **kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('main.index'))
        return route_func(*args, **kwargs)
    return wrapper