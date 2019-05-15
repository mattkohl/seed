from datetime import datetime

from app.spot.models import AlbumTuple
from . import db
from sqlalchemy.dialects.postgresql import JSON


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
    dbp_uri = db.Column(db.Text)
    mb_id = db.Column(db.Text)
    mb_obj = db.Column(JSON)
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
    dbp_uri = db.Column(db.Text)
    images_json = db.Column(JSON)
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

    def as_album_tuple(self):
        return AlbumTuple(uri=self.spot_uri, release_date=f"{self.release_date:%Y-%m-%d}", release_date_string=self.release_date_string, name=self.name, artists=list())


class Track(db.Model):
    __tablename__ = "tracks"
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    spot_uri = db.Column(db.Text)
    dbp_uri = db.Column(db.Text)
    name = db.Column(db.Text)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id', ondelete="CASCADE"))
    preview_url = db.Column(db.Text)
    lyrics = db.Column(db.Text)
    lyrics_url = db.Column(db.Text)
    lyrics_annotated = db.Column(db.Text)
    lyrics_annotations_json = db.Column(JSON)
    lyrics_fetched_timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    artists = db.relationship('Artist', secondary=track_artist, lazy='subquery',
                              backref=db.backref('artists_tracks', lazy=True))

    def __repr__(self):
        return f"<Track {self.name}>"

    def __str__(self):
        return f"TRACK: {self.name} [{self.album.name}] ({self.spot_uri})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
