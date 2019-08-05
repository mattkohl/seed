import traceback

from src import create_app, db
from src.models import Artist, Track, Album, Location, Genre


class Delete:

    @staticmethod
    def clear():
        try:
            Track.query.delete()
            Artist.query.delete()
            Album.query.delete()
            Genre.query.delete()
            Location.query.delete()
            db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    @staticmethod
    def delete_artist(_id: int):
        _artist = Artist.query.filter_by(id=_id).first()
        current = create_app('docker')
        with current.app_context():
            try:
                db.session.delete(_artist)
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            finally:
                db.session.close()

    @staticmethod
    def delete_track(track_id: int):
        _track = Track.query.filter_by(id=track_id).first()
        current = create_app('docker')
        with current.app_context():
            try:
                db.session.delete(_track)
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            finally:
                db.session.close()

    @staticmethod
    def delete_album(album_id: int):
        _album = Album.query.filter_by(id=album_id).first()
        current = create_app('docker')
        with current.app_context():
            try:
                db.session.delete(_album)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                traceback.print_tb(e.__traceback__)
                raise
            finally:
                db.session.close()

    @staticmethod
    def delete_sections(track_uri: str):
        _track = Track.query.filter_by(spot_uri=track_uri).first()
        current = create_app('docker')
        with current.app_context():
            try:
                db.session.add(_track)
                for _section in _track.sections:
                    db.session.delete(_section)
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            finally:
                db.session.close()

    @staticmethod
    def delete_hometown(artist_uri: str):
        _artist = Artist.query.filter_by(spot_uri=artist_uri).first()
        current = create_app('docker')
        with current.app_context():
            try:
                db.session.add(_artist)
                _artist.hometown = None
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            finally:
                db.session.close()

    @staticmethod
    def delete_birthplace(artist_uri: str):
        try:
            _artist = Artist.query.filter_by(spot_uri=artist_uri).first()
            current = create_app('docker')
            with current.app_context():
                db.session.add(_artist)
                _artist.birthplace = None
                db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        finally:
            db.session.close()
