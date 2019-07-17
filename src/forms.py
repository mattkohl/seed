from flask_wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, BooleanField
from wtforms.validators import DataRequired


class SearchForm(Form):
    search = StringField('search', validators=[DataRequired()])
    constrain_dates = BooleanField('Constrain Dates')


# class TrackForm(Form):
#     date = StringField('Release Date', validators=[DataRequired()])
#     artist = StringField('Primary Artist', validators=[DataRequired()])
#     title = StringField('Song Title', validators=[DataRequired()])
#     feat = StringField('Featured Artists')
#     album = StringField('Album Title', validators=[DataRequired()])
#     lyrics = TextAreaField('Lyrics', validators=[DataRequired()])
#     discogs_date = StringField('Discogs date')
#     rel_date_verified = StringField('Release Date Verified')
#     lyrics_verified = StringField('Lyrics Verified')
#     submit = SubmitField('Submit')
#
#     def from_model(self, song):
#         self.date.data = song.releaseDate
#         self.artist.data = song.artist
#         self.title.data = song.songTitle
#         self.feat.data = song.feat
#         self.album.data = song.album
#         self.lyrics.data = song.lyrics
#         self.discogs_date.data = song.discogsDate
#         self.rel_date_verified.data = song.relDateVerified
#         self.lyrics_verified.data = song.lyricsVerified
#
#     def to_model(self, song):
#         song.releaseDate = self.date.data
#         song.artist = self.artist.data
#         song.songTitle = self.title.data
#         song.feat = self.feat.data
#         song.album = self.album.data
#         song.lyrics = self.lyrics.data
#         song.discogsDate = self.discogs_date.data
#         song.relDateVerified = self.rel_date_verified.data
#         song.lyricsVerified = self.lyrics_verified.data


