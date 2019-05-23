from typing import Dict

from app import create_app, db
from app.models import Artist, Track, Album
from app.spot.models import TrackTuple, AlbumTuple


class Persist:

    @staticmethod
    def clear():
        Track.query.delete()
        Artist.query.delete()
        Album.query.delete()
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
    def persist_track_tuple(track: TrackTuple):
        current = create_app('docker')
        with current.app_context():
            _album = Persist.get_or_create(db.session, Album,
                                           name=track.album.name,
                                           spot_uri=track.album.uri,
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
            try:
                _album = Persist.get_or_create(db.session, Album,
                                               name=album.name,
                                               spot_uri=album.uri,
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
                for _artist in _artists:
                    _album.artists.append(_artist)
                db.session.commit()
