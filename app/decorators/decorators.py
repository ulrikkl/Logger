from functools import wraps
from flask import g, request, redirect, url_for, current_app
from app import db
from app.models import User
import os

def Setup_Required():
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            setup_status = current_app.config.get('SETUP_STATUS')
            if setup_status == None:
                return redirect(url_for('setup.register'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper

def Setup_Done():
    def wrapper(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            setup_status = current_app.config.get('SETUP_STATUS')
            if setup_status == "1":
                return redirect(url_for('main.index'))
            return f(*args, **kwargs)
        return decorated_function
    return wrapper