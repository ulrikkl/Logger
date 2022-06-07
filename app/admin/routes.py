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

@bp.route('/admin/log1', methods=['GET', 'POST'])
def log1():
    previewform = log_preview()
    form = log_test()
    if form.validate_on_submit():
        #previewform.json.data = [type(field) for field in form._fields.values()]
        data = {field.name: field.data for field in form._fields.values() if field.type not in ("SubmitField", "CSRFTokenField", "HiddenField")}
        jsonData = json.dumps(data)
        previewform.json.data = jsonData #{field.name: field.data for field in form._fields.values() if field.type not in ("SubmitField", "CSRFTokenField", "HiddenField")}
    return render_template('admin/log1.html', form=form, previewform=previewform)

@bp.route('/admin/form1', methods=['GET', 'POST'])
def form1():
    headerForm = log_header()
    headerForm.category.choices = [g.name for g in LogCat.query.all()]
    addForm = log_add_field()
    return render_template('admin/form1.html', 
        headerForm=headerForm, addForm=addForm)

@bp.route('/admin/form1/save', methods=['POST'])
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

@bp.route('/admin/form1/preview', methods=['POST'])
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

@bp.route('/admin/create_log')
def create_log():
    logForm = log_generate()
    return render_template('admin/create_log.html', logForm=logForm)

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