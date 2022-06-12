import json
from unicodedata import category

from sqlalchemy import JSON, Column
from app import db, login
from argon2 import PasswordHasher
from flask_login import UserMixin, current_user
from hashlib import md5

class User(db.Model, UserMixin):
    __tablename__= 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    roles = db.relationship('Role', secondary='user_roles')
    status = db.Column(db.String)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = PasswordHasher().hash(password)

    def check_password(self, password):
        return PasswordHasher().verify(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

# Define the Role data-model
class Role(db.Model):
        __tablename__ = 'roles'
        id = db.Column(db.Integer(), primary_key=True)
        name = db.Column(db.String(50), unique=True)

        def __repr__(self):
            return '<Role {}>'.format(self.name)

# Define the UserRoles association table
class UserRoles(db.Model):
        __tablename__ = 'user_roles'
        id = db.Column(db.Integer(), primary_key=True)
        user_id = db.Column(db.Integer(), db.ForeignKey('users.id', ondelete='CASCADE'))
        role_id = db.Column(db.Integer(), db.ForeignKey('roles.id', ondelete='CASCADE'))

class LogCat(db.Model):
    __tablename__ = 'log_categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    logs = db.relationship('Log', back_populates='category', lazy='dynamic')

    def __repr__(self):
         return '<Category {}>'.format(self.name)

class Log(db.Model):
    __tablename__ = 'log'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    message = db.Column(JSON)
    category_id = db.Column(db.Integer, db.ForeignKey('log_categories.id'))
    category = db.relationship('LogCat', back_populates='logs')

    def __repr__(self):
            return '<Log {}>'.format(self.name)
    
class ActiveLog(db.Model):
    __tablename__ = 'active_log'
    id = db.Column(db.Integer, primary_key=True)
    category = db.Column(db.String(50))
    type = db.Column(db.String(50))
    order = db.Column(db.Integer)
    message = db.Column(JSON)

    def set_location(self, orderId):
        self.order = orderId
