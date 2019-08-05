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
    def delete_track(_id: int):
        _track = Track.query.filter_by(id=_id).first()
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
    def delete_album(_id: int):
        current = create_app('docker')
        with current.app_context():
            try:
                _album = db.session.query(Album).filter(Album.id==_id).first()
                db.session.add(_album)
                db.session.delete(_album)
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                traceback.print_tb(e.__traceback__)
                raise
            finally:
                db.session.close()

    @staticmethod
    def delete_sections(uri):
        _track = Track.query.filter_by(spot_uri=uri).first()
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
    def delete_hometown(uri):
        _artist = Artist.query.filter_by(spot_uri=uri).first()
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
    def delete_birthplace(uri):
        try:
            _artist = Artist.query.filter_by(spot_uri=uri).first()
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
