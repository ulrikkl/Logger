from email import message
import sys
import json
import requests
import datetime
import hashlib
import hmac
import base64
from unicodedata import category
from flask import flash, redirect, render_template, session, url_for, request, Response, current_app
from flask_login import current_user, login_required, login_user, logout_user
from app import db
from app.models import User, Role, LogCat, ActiveLog, Log
from werkzeug.urls import url_parse
#from flask_user import roles_required
from app.main import bp
from sqlalchemy import func
from app.decorators.decorators import Setup_Required

@bp.route('/')
@bp.route('/index')
#@Setup_Required()
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

        log = ActiveLog.query.filter_by(order=orderId).first()
        log.message = message

        db.session.commit()

    return ('', 204)

def build_signature(customer_id, shared_key, date, content_length, method, content_type, resource):
    x_headers = 'x-ms-date:' + date
    string_to_hash = method + "\n" + str(content_length) + "\n" + content_type + "\n" + x_headers + "\n" + resource
    bytes_to_hash = bytes(string_to_hash, encoding="utf-8")  
    decoded_key = base64.b64decode(shared_key)
    encoded_hash = base64.b64encode(hmac.new(decoded_key, bytes_to_hash, digestmod=hashlib.sha256).digest()).decode()
    authorization = "SharedKey {}:{}".format(customer_id,encoded_hash)
    return authorization

def post_data(customer_id, shared_key, log_type, log_message):
    method = 'POST'
    content_type = 'application/json'
    resource = '/api/logs'
    rfc1123date = datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
    content_length = len(log_message)
    signature = build_signature(customer_id, shared_key, rfc1123date, content_length, method, content_type, resource)
    uri = 'https://' + customer_id + '.ods.opinsights.azure.com' + resource + '?api-version=2016-04-01'

    headers = {
        'content-type': content_type,
        'Authorization': signature,
        'Log-Type': log_type,
        'x-ms-date': rfc1123date
    }

    response = requests.post(uri,data=log_message, headers=headers)
    if (response.status_code >= 200 and response.status_code <= 299):
        return ("Log Sendt Succesfuldt")
    else:
        return ("Response code: {}, Error: {}, Message. {}".format(response.status_code, response.json()['Error'], response.json()['Message']))

@bp.route('/index/send', methods=['POST'])
def send_logs():
    if request.method == 'POST':
        data = request.get_json()['logs']
        
        customer_id = current_app.config.get('AZURE_WORKSPACE_ID')
        shared_key = current_app.config.get('AZURE_SHARED_KEY')
        msg = []
        for x in data:
            log_Type = x['type'].replace(" ", "_")
            log_Message = json.dumps(x['log'])

            response = post_data(customer_id, shared_key, log_Type, log_Message)
            msg.append(response)
        flash(msg[0])
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

