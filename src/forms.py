from flask_wtf import FlaskForm
from wtforms import StringField, BooleanField
from wtforms.validators import DataRequired


class SearchForm(FlaskForm):
    search = StringField('search', validators=[DataRequired()])
    constrain_dates = BooleanField('Constrain Dates')


class UriForm(FlaskForm):
    uri = StringField('uri', validators=[DataRequired()])


class TrackForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    lyrics = StringField('Lyrics')
    lyrics_annotated = StringField('Lyrics Annotated')
    lyrics_url = StringField('Lyrics Url')


class AlbumForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    release_date_string = StringField('Release Date String', validators=[DataRequired()])
    dbp_uri = StringField('DBPedia URI')
    wikipedia_uri = StringField('Wikipedia URI')


class ArtistForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    dbp_uri = StringField('DBPedia URI')
    wikipedia_uri = StringField('Wikipedia URI')

