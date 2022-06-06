from flask import flash, redirect, render_template, url_for, request
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from app.models import User, Role, LogCat
from werkzeug.urls import url_parse
#from flask_user import roles_required
from app.main import bp

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    logs = [
        {
            'type': "SecurityEvent",
            'message': "4625"
        },
        {
            'type': "SecurityEvent",
            'message': "4624"
        }
    ]
    return render_template('index.html', title='Home', logs=logs)

@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user/user.html', user=user)