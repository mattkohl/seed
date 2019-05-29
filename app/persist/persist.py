from typing import Dict

from app import create_app, db
from app.dbp.models import LocationTuple
from app.models import Artist, Track, Album, Location, Genre
from app.spot.models import TrackTuple, AlbumTuple, GenreTuple, ArtistTuple


class Persist:

    @staticmethod
    def clear():
        Track.query.delete()
        Artist.query.delete()
        Album.query.delete()
        Genre.query.delete()
        Location.query.delete()
        db.session.commit()

    @staticmethod
    def get_or_create(session, model: db.Model, **kwargs) -> db.Model:
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    @staticmethod
    def update(model: db.Model, _id: int, _updates: Dict):
        current = create_app('docker')
        with current.app_context():
            db.session.query(model).filter(model.id == _id).update(_updates)
            db.session.commit()

    @staticmethod
    def persist_artist_tuple(artist: ArtistTuple):
        current = create_app('docker')
        with current.app_context():
            _artist = Persist.get_or_create(db.session, Artist,
                                            name=artist.name,
                                            spot_uri=artist.uri)

            _genres = [Persist.get_or_create(db.session, Genre, name=genre.name) for genre in artist.genres]
            db.session.add(_artist)
            _artist.genres.extend(_genres)
            db.session.commit()

    @staticmethod
    def persist_track_tuple(track: TrackTuple):
        current = create_app('docker')
        with current.app_context():
            img = track.album.images[0]["url"] if track.album.images else None
            thumb = track.album.images[-1]["url"] if track.album.images and len(track.album.images) > 1 else None
            _album = Persist.get_or_create(db.session, Album,
                                           name=track.album.name,
                                           spot_uri=track.album.uri,
                                           img=img,
                                           thumb=thumb,
                                           release_date=track.album.release_date,
                                           release_date_string=track.album.release_date_string,
                                           )
            _track = Persist.get_or_create(db.session, Track,
                                           name=track.name,
                                           spot_uri=track.uri,
                                           preview_url=track.preview_url,
                                           album_id=_album.id)
            _primary_artists = [Persist.get_or_create(db.session, Artist,
                                                      name=artist.name,
                                                      spot_uri=artist.uri)
                                for artist in track.primary_artists]
            _featured_artists = [Persist.get_or_create(db.session, Artist,
                                                       name=artist.name,
                                                       spot_uri=artist.uri)
                                 for artist in track.featured_artists]

            db.session.add(_track)

            _album.artists.extend(_primary_artists)
            _track.primary_artists.extend(_primary_artists)
            _track.featured_artists.extend(_featured_artists)

            db.session.commit()

    @staticmethod
    def persist_album_tuple(album: AlbumTuple):
        current = create_app('docker')
        with current.app_context():
            img = album.images[0]["url"] if album.images else None
            thumb = album.images[-1]["url"] if len(album.images) > 1 else None

            try:
                _album = Persist.get_or_create(db.session, Album,
                                               name=album.name,
                                               spot_uri=album.uri,
                                               img=img,
                                               thumb=thumb,
                                               release_date=album.release_date,
                                               release_date_string=album.release_date_string,
                                               )
                _artists = [Persist.get_or_create(db.session, Artist,
                                                  name=artist.name,
                                                  spot_uri=artist.uri)
                            for artist in album.artists]

            except Exception:
                raise
            else:
                db.session.add(_album)
                if _artists:
                    _album.artists.extend(_artists)
                db.session.commit()

    @staticmethod
    def persist_genre_tuple(genre: GenreTuple) -> None:
        current = create_app('docker')
        with current.app_context():
            try:
                _genre = Persist.get_or_create(db.session, Genre, name=genre.name)
            except Exception:
                raise
            else:
                db.session.add(_genre)
                db.session.commit()

    @staticmethod
    def persist_location_tuple(location: LocationTuple) -> None:
        current = create_app('docker')
        with current.app_context():
            try:
                _location = Persist.get_or_create(db.session, Location,
                                                  name=location.label,
                                                  dbp_uri=location.uri,
                                                  latitude=location.latitude,
                                                  longitude=location.longitude,
                                                  )

            except Exception:
                raise
            else:
                db.session.add(_location)
                if location.hometown_of is not None:
                    _location.hometown_of = [location.hometown_of]
                if location.birthplace_of is not None:
                    _location.birthplace_of = [location.birthplace_of]
                db.session.commit()

    @staticmethod
    def delete_hometown(uri):
        _artist = Artist.query.filter_by(spot_uri=uri).first()
        current = create_app('docker')
        with current.app_context():
            db.session.add(_artist)
            _artist.hometown = None
            db.session.commit()

    @staticmethod
    def delete_birthplace(uri):
        _artist = Artist.query.filter_by(spot_uri=uri).first()
        current = create_app('docker')
        with current.app_context():
            db.session.add(_artist)
            _artist.birthplace = None
            db.session.commit()
