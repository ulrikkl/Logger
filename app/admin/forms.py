import imp
from flask import Flask
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, HiddenField, SelectField
from wtforms.validators import DataRequired, ValidationError

class log_test(FlaskForm):
    event_id = StringField('Event ID')
    activity = StringField('Activity')

    submit = SubmitField('Submit')

class log_preview(FlaskForm):
    json = TextAreaField('JSON', render_kw={'readonly': True})


class log_header(FlaskForm):
    category = SelectField("Category", validators=[DataRequired()])
    type = StringField('Type', validators=[DataRequired()])

class log_empty(FlaskForm):
    temp = HiddenField('Temp Field')

class log_add_field(FlaskForm):
    newFieldName = StringField('New Field Name')
    addNewField = SubmitField('Add Field')

class log_save_field(FlaskForm):
    saveLog = SubmitField('Save Log')

class log_generate(FlaskForm):
    inputField = TextAreaField('Input')
    submit = SubmitField('Submit')

class add_cat(FlaskForm):
    newCat = StringField("Category Name")
    submit = SubmitField("Submit")

class del_cat(FlaskForm):
    delete = SubmitField("Delete")