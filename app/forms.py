from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from flask import request


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')
 

class SearchForm(FlaskForm):
    id = StringField('Request for a ticket with ID', validators=[DataRequired()])
    submit = SubmitField('Go')

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)