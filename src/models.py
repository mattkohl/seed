from datetime import datetime
from typing import List

from src.spot.models import AlbumTuple, ArtistTuple, GenreTuple
from src.utils import Utils
from . import db
from sqlalchemy.dialects.postgresql import JSON


track_primary_artist = \
    db.Table('track_primary_artist',
             db.Column('track_id', db.Integer, db.ForeignKey('tracks.id', ondelete="CASCADE"), primary_key=True),
             db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', ondelete="CASCADE"), primary_key=True))


track_featured_artist = \
    db.Table('track_featured_artist',
             db.Column('track_id', db.Integer, db.ForeignKey('tracks.id', ondelete="CASCADE"), primary_key=True),
             db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', ondelete="CASCADE"), primary_key=True))


section_artist = \
    db.Table('section_artist',
             db.Column('section_id', db.Integer, db.ForeignKey('sections.id', ondelete="CASCADE"), primary_key=True),
             db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', ondelete="CASCADE"), primary_key=True))


artist_hometown = \
    db.Table('artist_hometown',
             db.Column('location_id', db.Integer, db.ForeignKey('locations.id', ondelete="CASCADE"), primary_key=True),
             db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', ondelete="CASCADE"), primary_key=True))


artist_birthplace = \
    db.Table('artist_birthplace',
             db.Column('location_id', db.Integer, db.ForeignKey('locations.id', ondelete="CASCADE"), primary_key=True),
             db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', ondelete="CASCADE"), primary_key=True))


album_artist = \
    db.Table('album_artist',
             db.Column('album_id', db.Integer, db.ForeignKey('albums.id', ondelete="CASCADE"), primary_key=True),
             db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', ondelete="CASCADE"), primary_key=True))


artist_genre = \
    db.Table('artist_genre',
             db.Column('artist_id', db.Integer, db.ForeignKey('artists.id', ondelete="CASCADE"), primary_key=True),
             db.Column('genre_id', db.Integer, db.ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True))


album_genre = \
    db.Table('album_genre',
             db.Column('album_id', db.Integer, db.ForeignKey('albums.id', ondelete="CASCADE"), primary_key=True),
             db.Column('genre_id', db.Integer, db.ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True))


track_genre = \
    db.Table('track_genre',
             db.Column('track_id', db.Integer, db.ForeignKey('tracks.id', ondelete="CASCADE"), primary_key=True),
             db.Column('genre_id', db.Integer, db.ForeignKey('genres.id', ondelete="CASCADE"), primary_key=True))


class Artist(db.Model):
    __tablename__ = "artists"
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    spot_uri = db.Column(db.Text)
    dbp_uri = db.Column(db.Text)
    mb_id = db.Column(db.Text)
    mb_obj = db.Column(JSON)
    img = db.Column(db.Text)
    thumb = db.Column(db.Text)
    name = db.Column(db.Text)
    primary_tracks = db.relationship('Track', secondary=track_primary_artist, lazy='subquery', backref=db.backref('primary_artists', lazy=True))
    featured_tracks = db.relationship('Track', secondary=track_featured_artist, lazy='subquery', backref=db.backref('featured_artists', lazy=True))
    sections = db.relationship('Section', secondary=section_artist, lazy='subquery', backref=db.backref('section_artists', lazy=True))
    albums = db.relationship('Album', secondary=album_artist, lazy='subquery', backref=db.backref('albums_artists', lazy='dynamic'))
    hometown = db.relationship('Location', secondary=artist_hometown, lazy='subquery', uselist=False, backref=db.backref('hometown_of', lazy='dynamic'))
    birthplace = db.relationship('Location', secondary=artist_birthplace, lazy='subquery', uselist=False, backref=db.backref('birthplace_of', lazy='dynamic'))
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Artist {self.name}>"

    def __str__(self):
        return f"ARTIST: {self.name} ({self.spot_uri})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_artist_tuple(self):
        return ArtistTuple(uri=self.spot_uri, name=self.name)


class Location(db.Model):
    __tablename__ = "locations"
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    dbp_uri = db.Column(db.Text)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Location {self.name}>"

    def __str__(self):
        return f"LOCATION: {self.name} ({self.latitude}, {self.longitude}) <{self.dbp_uri}>"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Album(db.Model):
    __tablename__ = "albums"
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    release_date_string = db.Column(db.Text)
    release_date = db.Column(db.DateTime)
    spot_uri = db.Column(db.Text)
    dbp_uri = db.Column(db.Text)
    mb_id = db.Column(db.Text)
    mb_obj = db.Column(JSON)
    img = db.Column(db.Text)
    thumb = db.Column(db.Text)
    name = db.Column(db.Text)
    tracks = db.relationship('Track', backref='album', lazy='dynamic')
    artists = db.relationship('Artist', secondary=album_artist, lazy='subquery',
                              backref=db.backref('artists_albums', lazy=True))
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Album {self.name}>"

    def __str__(self):
        return f"ALBUM: {self.name} ({self.spot_uri})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_tuple_dict(self, artists: List[Artist]):
        exclusions = ["created", "dbp_uri", "mb_id", "mb_obj", "img", "thumb", "last_updated"]
        _raw = {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in exclusions}
        _uri = _raw.pop("spot_uri")
        _raw.update({"artists": [{"name": _artist.name, "uri": _artist.spot_uri} for _artist in artists], "uri": _uri})
        return Utils.format_dates(_raw)

    def as_album_tuple(self, artists: List[Artist]):
        return AlbumTuple(
            uri=self.spot_uri,
            release_date=f"{self.release_date:%Y-%m-%d}",
            release_date_string=self.release_date_string,
            name=self.name,
            artists=[_a.as_artist_tuple()._asdict() for _a in artists]
        )


class Genre(db.Model):
    __tablename__ = "genres"
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    dbp_uri = db.Column(db.Text)
    mb_id = db.Column(db.Text)
    mb_obj = db.Column(JSON)
    name = db.Column(db.Text)
    artists = db.relationship('Artist', secondary=artist_genre, lazy='subquery', backref=db.backref('genres', lazy=True))
    albums = db.relationship('Album', secondary=album_genre, lazy='subquery', backref=db.backref('genres', lazy='dynamic'))
    tracks = db.relationship('Track', secondary=track_genre, lazy='subquery', backref=db.backref('genres', lazy=True))
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Genre {self.name}>"

    def __str__(self):
        return f"GENRE: {self.name}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def as_genre_tuple(self):
        return GenreTuple(id=self.id, name=self.name)


class Track(db.Model):
    __tablename__ = "tracks"
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    spot_uri = db.Column(db.Text)
    dbp_uri = db.Column(db.Text)
    mb_id = db.Column(db.Text)
    mb_obj = db.Column(JSON)
    name = db.Column(db.Text)
    album_id = db.Column(db.Integer, db.ForeignKey('albums.id', ondelete="CASCADE"))
    preview_url = db.Column(db.Text)
    lyrics = db.Column(db.Text)
    lyrics_url = db.Column(db.Text)
    lyrics_annotated = db.Column(db.Text)
    lyrics_annotations_json = db.Column(JSON)
    sections = db.relationship('Section', backref='track', lazy='dynamic')
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Track {self.name}>"

    def __str__(self):
        return f"TRACK: {self.name} [{self.album.name}] ({self.spot_uri})"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Section(db.Model):
    __tablename__ = "sections"
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    id = db.Column(db.Integer, primary_key=True)
    track_id = db.Column(db.Integer, db.ForeignKey('tracks.id', ondelete="CASCADE"))
    type = db.Column(db.Text)
    number = db.Column(db.Integer)
    artists_raw = db.Column(db.Text)
    text = db.Column(db.Text)
    text_annotated = db.Column(db.Text)
    offset = db.Column(db.Integer)
    last_updated = db.Column(db.DateTime)

    def __repr__(self):
        return f"<Section {self.name}>"

    def __str__(self):
        return f"SECTION {self.offset} [{self.artists_raw}]: {self.text}"

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}