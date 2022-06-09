from crypt import methods
from flask import redirect, render_template, request, url_for, flash, jsonify
from app import db
from app.models import User, Role, LogCat, Log
from app.admin import bp
from app.admin.forms import log_preview, log_test, log_header, log_add_field, log_generate, add_cat, del_cat
import sys
import json

@bp.route('/admin/')
@bp.route('/admin/control_panel')
#@roles_required('Admin')
def control_panel():
    cats = LogCat.query.all()
    return render_template('admin/control_panel.html', title='Control Panel', 
    cats=cats)

@bp.route('/admin/create_log', methods=['GET', 'POST'])
def create_log():
    headerForm = log_header()
    headerForm.category.choices = [g.name for g in LogCat.query.all()]
    addForm = log_add_field()
    return render_template('admin/create_log.html', 
        headerForm=headerForm, addForm=addForm)

@bp.route('/admin/create_log/save', methods=['POST'])
def save_log():
    if request.method == 'POST':
        jsonData = request.get_json()

        logCat = jsonData['cat']
        logType = jsonData['type']
        message = jsonData['message']

        messageList = []
        for x in message:
            value = x.get('value')
            messageList.append(value)
        
        logDict = dict.fromkeys(messageList)
        logJson = json.dumps(logDict)

        log = Log(name=logType, message=logJson)
        cat = LogCat.query.filter_by(name=logCat).first()

        log.category_id = cat.id
        db.session.add(log)
        db.session.commit()

        print(logCat, file=sys.stderr)
        print(logType, file=sys.stderr)
        print(logJson, file=sys.stderr)

        flash('New log saved Successfully')
        msg = "New log saved successfully"
    return jsonify(msg)

@bp.route('/admin/create_log/preview', methods=['POST'])
def preview_log():
    if request.method == 'POST':
        jsonData = request.get_json()
        message = jsonData['message']
        messageList = []
        for x in message:
            value = x.get('value')
            messageList.append(value)

        logDict = dict.fromkeys(messageList)
        logJson = json.dumps(logDict)
    return jsonify(logJson)

@bp.route('/admin/user_requests', methods=['GET', 'POST'])
def user_requests():
    users = User.query.filter_by(status='Inactive').all()
    return render_template('admin/user_requests.html', users=users)

@bp.route('/admin/user_requests/accept', methods=['GET', 'POST'])
def accept_user():
    userId = request.form['user_to_accept']
    user = User.query.filter_by(id=userId).first()
    user.status = "Active"
    db.session.commit()
    flash("User accepted successfully")
    return redirect(url_for('admin.user_requests'))

@bp.route('/admin/list_logs')
def list_logs():
    cats = LogCat.query.all()
    return render_template('admin/list_logs.html', cats=cats)

@bp.route('/admin/list_logs/delete', methods=['GET', 'POST'])
def del_log():
    logId = request.form['log_to_delete']
    log = Log.query.filter_by(id=logId).first()
    db.session.delete(log)
    db.session.commit()
    flash("Log removed successfully")
    return redirect(url_for('admin.list_logs'))

@bp.route('/admin/list_categories', methods=['GET', 'POST'])
def list_categories():
    addCat = add_cat()
    delCat = del_cat()
    cats = LogCat.query.all()
    if addCat.validate_on_submit():
        cat = LogCat(name=addCat.newCat.data)
        db.session.add(cat)
        db.session.commit()
        flash("Category added successfully")
        return redirect(url_for('admin.list_categories'))
    return render_template('admin/list_categories.html', cats=cats, addCat=addCat, delCat=delCat)

@bp.route('/admin/list_categories/delete', methods=['GET', 'POST'])
def del_category():
    catId = request.form['cat_to_delete']
    cat = LogCat.query.filter_by(id=catId).first()
    db.session.delete(cat)
    db.session.commit()
    flash("Category removed successfully")
    return redirect(url_for('admin.list_categories'))

@bp.route('/admin/list_users', methods=['GET', 'POST'])
def list_users():
    users = User.query.order_by(User.status.asc()).all()
    return render_template('admin/list_users.html', users=users)

@bp.route('/admin/list_users/delete', methods=['GET', 'POST'])
def del_user():
    userId = request.form['user_to_accept']
    user = User.query.filter_by(id=userId).first()
    db.session.delete(user)
    db.session.commit()
    flash("User deleted successfully")
    return redirect(url_for('admin.user_requests'))