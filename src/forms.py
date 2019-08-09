from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    constrain_dates = BooleanField('Constrain Dates')


class UriForm(FlaskForm):
    uri = StringField('uri', validators=[DataRequired()])
