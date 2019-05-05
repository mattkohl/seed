from typing import Dict

from app import create_app, db
from app.models import Artist, Track, Album
from app.spot.models import TrackTuple


class Persist:

    @staticmethod
    def get_or_create(session, model, **kwargs) -> db.Model:
        instance = session.query(model).filter_by(**kwargs).first()
        if instance:
            return instance
        else:
            instance = model(**kwargs)
            session.add(instance)
            session.commit()
            return instance

    @staticmethod
    def update_track(track_id: int, updates: Dict):
        current = create_app('docker')
        with current.app_context():
            db.session.query(Track).filter(Track.id == track_id).update(updates)
            db.session.commit()

    @staticmethod
    def persist_track(track: TrackTuple):
        current = create_app('docker')
        with current.app_context():
            _album = Persist.get_or_create(db.session, Album,
                                           name=track.album.name,
                                           spot_uri=track.album.uri,
                                           release_date=track.album.release_date,
                                           release_date_string=track.album.release_date_string)
            _track = Persist.get_or_create(db.session, Track,
                                           name=track.name,
                                           spot_uri=track.uri,
                                           preview_url=track.preview_url,
                                           album_id=_album.id)
            _artists = [Persist.get_or_create(db.session, Artist,
                                              name=artist.name,
                                              spot_uri=artist.uri)
                        for artist in track.artists]
            db.session.add(_track)
            for _artist in _artists:
                _track.artists.append(_artist)
                _artist.albums.append(_album)
            db.session.commit()
