from flask import Blueprint

bp = Blueprint('decorators', __name__)

from app.decorators import decorators