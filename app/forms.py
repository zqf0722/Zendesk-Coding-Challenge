from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import NumberRange
from flask import request


class SearchForm(FlaskForm):
    id = IntegerField('Request with ID', [NumberRange(min=1)])
    submit = SubmitField('Go')

    def __init__(self, *args, **kwargs):
        if 'formdata' not in kwargs:
            kwargs['formdata'] = request.args
        if 'csrf_enabled' not in kwargs:
            kwargs['csrf_enabled'] = False
        super(SearchForm, self).__init__(*args, **kwargs)