from datetime import datetime
from . import db


song_artist = db.Table('SongArtist',
                       db.Column('song_id', db.Integer, db.ForeignKey('song.id'), primary_key=True),
                       db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True))


album_artist = db.Table('AlbumArtist',
                        db.Column('album_id', db.Integer, db.ForeignKey('album.id'), primary_key=True),
                        db.Column('artist_id', db.Integer, db.ForeignKey('artist.id'), primary_key=True))


class Artist(db.Model):
    __tablename__ = "artists"
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    spot_uri = db.Column(db.Text)
    name = db.Column(db.Text)
    songs = db.relationship('Song', secondary=song_artist, lazy='subquery', backref=db.backref('artists', lazy=True))
    albums = db.relationship('Album', secondary=album_artist, lazy='subquery', backref=db.backref('artists', lazy=True))

    def __repr__(self):
        return f"<Artist {self.name}>"


class Album(db.Model):
    __tablename__ = "albums"
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    release_date_string = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    spot_uri = db.Column(db.Text)
    name = db.Column(db.Text)
    artists = db.relationship('Artist', secondary=album_artist, lazy='subquery',
                              backref=db.backref('albums', lazy=True))

    def __repr__(self):
        return f"<Album {self.name}>"


class Song(db.Model):
    __tablename__ = "songs"
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    spot_uri = db.Column(db.Text)
    name = db.Column(db.Text)
    album = db.Column(db.Integer, db.ForeignKey('albums.id'))
    popularity = db.Column(db.Integer)
    preview_url = db.Column(db.Text)
    lyrics = db.Column(db.Text)
    artists = db.relationship('Artist', secondary=song_artist, lazy='subquery',
                              backref=db.backref('songs', lazy=True))

    def __repr__(self):
        return f"<Album {self.name}>"
