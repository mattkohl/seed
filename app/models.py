from datetime import datetime
from . import db


class Artist(db.Model):
    __tablename__ = "artists"
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    spot_uri = db.Column(db.Text)
    name = db.Column(db.Text)


class Song(db.Model):
    __tablename__ = "songs"
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    spot_uri = db.Column(db.Text)
    release_date_string = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    primary_artists = db.relationship('Artist', backref='primary_songs', lazy='dynamic')
    featured_artists = db.relationship('Artist', backref='featured_songs', lazy='dynamic')
    title = db.Column(db.Text)
    album = db.Column(db.Text)
    lyrics = db.Column(db.Text)
