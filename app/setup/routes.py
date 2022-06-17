from flask import render_template, redirect, url_for, flash, request, current_app
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db
from app.setup import bp
from app.setup.forms import RegistrationForm, AzureConfigForm
from app.models import User, Role
from app.decorators.decorators import Setup_Done
import signal
import os
import dotenv

@bp.route('/setup/register', methods=['GET', 'POST'])
@Setup_Done()
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        role = Role(name="Admin")
        db.session.add(role)
        role = Role.query.filter_by(name='Admin').first()
        user.roles.append(role)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('setup.conf_azure'))
    return render_template('setup/register.html', title='Register', form=form)

@bp.route('/setup/azure' , methods=['GET', 'POST'])
@Setup_Done()
def conf_azure():
    form = AzureConfigForm()
    dotenv_path = "/home/logger/.env"
    if form.validate_on_submit():
        # os.environ['SETUP_STATUS'] = "1"
        # os.environ['WORKSPACE_ID'] = form.workspaceId.data
        # os.environ['SHARED_KEY'] = form.sharedKey.data
        dotenv.set_key(dotenv_path, "SETUP_STATUS", "1")
        dotenv.set_key(dotenv_path, "WORKSPACE_ID", form.workspaceId.data)
        dotenv.set_key(dotenv_path, "SHARED_KEY", form.sharedKey.data)
        # workspaceId = form.workspaceId.data
        # sharedKey = form.sharedKey.data
        # configData = "SETUP_STATUS=1" + "\nWORKSPACE_ID="+ workspaceId + "\nSHARED_KEY=" + sharedKey
        # fo = open('.env', 'w')
        # fo.write(configData)
        # fo.close()
        pid = os.getpid()
        sig = signal.SIGHUP
        os.kill(pid, sig)
        return redirect(url_for('auth.login'))
    return render_template('setup/config.html', title='Register', form=form)

