from datetime import datetime
from . import db


track_artist = db.Table('track_artist',
                       db.Column('track_id', db.Integer, db.ForeignKey('tracks.id', ondelete="CASCADE"), primary_key=True),
                       db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', ondelete="CASCADE"), primary_key=True))


album_artist = db.Table('album_artist',
                        db.Column('album_id', db.Integer, db.ForeignKey('albums.id', ondelete="CASCADE"), primary_key=True),
                        db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', ondelete="CASCADE"), primary_key=True))


class Artist(db.Model):
    __tablename__ = "artists"
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    spot_uri = db.Column(db.Text)
    name = db.Column(db.Text)
    tracks = db.relationship('Track', secondary=track_artist, lazy='subquery', backref=db.backref('tracks_artists', lazy=True))
    albums = db.relationship('Album', secondary=album_artist, lazy='subquery', backref=db.backref('albums_artists', lazy=True))

    def __repr__(self):
        return f"<Artist {self.name}>"

    def __str__(self):
        return f"ARTIST: {self.name} ({self.spot_uri})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Album(db.Model):
    __tablename__ = "albums"
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    release_date_string = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    spot_uri = db.Column(db.Text)
    name = db.Column(db.Text)
    tracks = db.relationship('Track', backref='album', lazy=True)
    artists = db.relationship('Artist', secondary=album_artist, lazy='subquery',
                              backref=db.backref('artists_albums', lazy=True))

    def __repr__(self):
        return f"<Album {self.name}>"

    def __str__(self):
        return f"ALBUM: {self.name} ({self.spot_uri})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Track(db.Model):
    __tablename__ = "tracks"
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    spot_uri = db.Column(db.Text)
    name = db.Column(db.Text)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id', ondelete="CASCADE"))
    popularity = db.Column(db.Integer)
    preview_url = db.Column(db.Text)
    lyrics = db.Column(db.Text)
    artists = db.relationship('Artist', secondary=track_artist, lazy='subquery',
                              backref=db.backref('artists_tracks', lazy=True))

    def __repr__(self):
        return f"<Track {self.name}>"

    def __str__(self):
        return f"TRACK: {self.name} [{self.album.name}] ({self.spot_uri})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
