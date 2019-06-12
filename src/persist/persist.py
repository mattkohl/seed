from datetime import datetime
from typing import Dict

from src.geni.models import SectionTuple
from src import create_app, db
from src.dbp.models import LocationTuple
from src.models import Artist, Track, Album, Location, Genre, Section
from src.spot.models import TrackTuple, AlbumTuple, GenreTuple, ArtistTuple


class Persist:

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
    def get_or_create(session, model: db.Model, **kwargs) -> db.Model:
        try:
            instance = session.query(model).filter_by(**kwargs).first()
            if instance:
                return instance
            else:
                instance = model(**kwargs)
                session.add(instance)
                session.commit()
                return instance
        except Exception:
            session.rollback()
            raise

    @staticmethod
    def update(model: db.Model, _id: int, _updates: Dict):
        current = create_app('docker')
        with current.app_context():
            try:
                _updates.update({model.last_updated: datetime.utcnow()})
                db.session.query(model).filter(model.id == _id).update(_updates)
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            finally:
                db.session.close()

    @staticmethod
    def persist_artist_tuple(artist: ArtistTuple):
        current = create_app('docker')
        with current.app_context():
            try:
                _artist = Persist.get_or_create(db.session, Artist,
                                                name=artist.name,
                                                spot_uri=artist.uri)

                _genres = [Persist.get_or_create(db.session, Genre, name=genre.name) for genre in artist.genres] if artist.genres else None
                _artist.img = artist.images[0]["url"] if artist.images else None
                _artist.thumb = artist.images[-1]["url"] if len(artist.images) > 1 else None
                db.session.add(_artist)
                if _genres:
                    _artist.genres.extend(_genres)
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            finally:
                db.session.close()

    @staticmethod
    def persist_section_tuple(section: SectionTuple, track_id: int):
        current = create_app('docker')
        with current.app_context():
            try:
                _section = Persist.get_or_create(db.session, Section,
                                                 track_id=track_id,
                                                 number=section.number)
                db.session.add(_section)
                _section.type = section.type
                _section.offset = section.offset
                _section.artists_raw = section.artists
                _section.text = section.text
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            finally:
                db.session.close()

    @staticmethod
    def persist_track_tuple(track: TrackTuple):
        current = create_app('docker')
        with current.app_context():
            try:
                img = track.album.images[0]["url"] if track.album.images else None
                thumb = track.album.images[-1]["url"] if track.album.images and len(track.album.images) > 1 else None
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
                db.session.add(_album)
                _album.img = img
                _album.thumb = thumb
                _album.artists.extend(_primary_artists)
                _track.primary_artists.extend(_primary_artists)
                _track.featured_artists.extend(_featured_artists)
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            finally:
                db.session.close()

    @staticmethod
    def persist_album_tuple(album: AlbumTuple):
        try:
            current = create_app('docker')
            with current.app_context():
                img = album.images[0]["url"] if album.images else None
                thumb = album.images[-1]["url"] if len(album.images) > 1 else None
                _genres = [Persist.get_or_create(db.session, Genre, name=genre.name) for genre in album.genres] if album.genres else None
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
                db.session.commit()
                _album.img = img
                _album.thumb = thumb
                if _artists:
                    _album.artists.extend(_artists)
                if _genres:
                    _album.genres.extend(_genres)
                db.session.commit()
        except Exception:
            db.session.rollback()
            raise
        finally:
            db.session.close()

    @staticmethod
    def persist_genre_tuple(genre: GenreTuple) -> None:
        current = create_app('docker')
        with current.app_context():
            try:
                _genre = Persist.get_or_create(db.session, Genre, name=genre.name)
                db.session.add(_genre)
                db.session.commit()
            except Exception:
                db.session.rollback()
                raise
            finally:
                db.session.close()

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
                db.session.add(_location)
                if location.hometown_of is not None:
                    _location.hometown_of = [location.hometown_of]
                if location.birthplace_of is not None:
                    _location.birthplace_of = [location.birthplace_of]
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