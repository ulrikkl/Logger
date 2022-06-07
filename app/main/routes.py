import sys
import json
from unicodedata import category
from flask import flash, redirect, render_template, session, url_for, request, Response
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from app.models import User, Role, LogCat, ActiveLog, Log
from werkzeug.urls import url_parse
#from flask_user import roles_required
from app.main import bp
from sqlalchemy import func

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    cats = LogCat.query.all()
    activeLogs = ActiveLog.query.order_by(ActiveLog.order.asc()).all()
    return render_template('index.html', title='Home', cats=cats, activeLogs=activeLogs)

@bp.route('/index/add', methods=['POST'])
def add_log():
    if request.method == 'POST':
        logId = request.get_data(as_text=True)
        log = Log.query.filter_by(id=logId).first_or_404()

        orderNr = db.session.query(func.max(ActiveLog.order)).first()[0]
        if orderNr is not None:
            orderNr += 1
        else:
            orderNr = 1
        
        addLog = ActiveLog(category=log.category.name, type=log.name, message=log.message, order=orderNr)
        db.session.add(addLog)
        db.session.commit()
    return ('', 204)

@bp.route('/index/rem', methods=['POST'])
def rem_log():
    if request.method == 'POST':
        logId = request.get_data(as_text=True)
        remLog = ActiveLog.query.filter_by(id=logId).first()
        remLogLoc = remLog.order

        ActiveLog.query.filter_by(id=logId).delete()
        logs = ActiveLog.query.filter(ActiveLog.order>remLogLoc).all()
        num = 1
        for log in logs:
            log.set_location(log.order-num)
        db.session.commit()
    return ('', 204)

@bp.route('/index/movup', methods=['POST'])
def mov_up():
    if request.method == 'POST':
        logId = request.get_data(as_text=True)

        firstLog = ActiveLog.query.filter_by(id=logId).first()
        firstLogLoc = firstLog.order
        secondLog = ActiveLog.query.filter_by(order=firstLogLoc-1).first()

        if secondLog is not None:
            temp = firstLogLoc
            firstLog.set_location(secondLog.order)
            secondLog.set_location(temp)
            db.session.commit()
        
    return ('', 204)


@bp.route('/index/movdown', methods=['POST'])
def mov_down():
    if request.method == 'POST':
        logId = request.get_data(as_text=True)

        firstLog = ActiveLog.query.filter_by(id=logId).first()
        firstLogLoc = firstLog.order
        secondLog = ActiveLog.query.filter_by(order=firstLogLoc+1).first()

        if secondLog is not None:
            temp = firstLogLoc
            firstLog.set_location(secondLog.order)
            secondLog.set_location(temp)
            db.session.commit()
        
    return ('', 204)

@bp.route('/index/save', methods=['POST'])
def autosave_form():
    if request.method == 'POST':
        jsonData = request.get_json()

        orderId = jsonData['orderId']
        message = jsonData['message']

        print(message, file=sys.stderr)
        log = ActiveLog.query.filter_by(order=orderId).first()
        log.message = message

        db.session.commit()

    return ('', 204)

@bp.route('/index/send', methods=['POST'])
def send_logs():
    if request.method == 'POST':
        data = request.form.getlist("logs[]")
        for log in data:
            print(log, file=sys.stderr)
    return ('', 204)

@bp.route('/index/clear', methods=['POST','GET'])
def clear_logs():
    if request.method == 'POST':
        ActiveLog.query.delete()
        db.session.commit()
    return ('', 204)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('user/user.html', user=user)