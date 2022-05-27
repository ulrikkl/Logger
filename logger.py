from app import app, db
from app.models import User, Role, UserRoles

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Role': Role, 'UserRoles': UserRoles}