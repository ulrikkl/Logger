from functools import wraps
from flask import g, request, redirect, url_for, current_app
from app import db
from app.models import User

def Setup_Required():
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_app.config.get('SETUP_STATUS') == "0" or current_app.config.get('SETUP_STATUS') == None:
                return redirect(url_for('setup.register'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def Setup_Done():
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if current_app.config.get('SETUP_STATUS') == "1":
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper