from typing import Optional
import traceback

from src import db
from src.dbp.models import CandidatesTuple, AnnotationTuple, LocationTuple
from src.models import Track, Artist, Album, Location, Genre
from src.persist.persist import Persist
from src.spot.models import TrackTuple, AlbumTuple, ArtistTuple


class Persistence:

    @staticmethod
    def clear():
        message = f"Deleted " \
            f"{Track.query.count()} Tracks, " \
            f"{Artist.query.count()} Artists, " \
            f"{Album.query.count()} Albums, " \
            f"{Genre.query.count()} Genres, & " \
            f"{Location.query.count()} Locations"
        try:
            Persist.clear()
        except Exception as e:
            print(f"Unable to delete everything")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return {"status": message}

    @staticmethod
    def persist_track(track_tuple: TrackTuple) -> None:
        try:
            Persist.persist_track_tuple(track_tuple)
        except Exception as e:
            print(f"Unable to persist track {track_tuple}")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def persist_album(album_tuple: AlbumTuple) -> None:
        try:
            Persist.persist_album_tuple(album_tuple)
        except Exception as e:
            print(f"Unable to persist track {album_tuple}")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def persist_location(location_tuple: LocationTuple) -> None:
        try:
            Persist.persist_location_tuple(location_tuple)
        except Exception as e:
            print(f"Unable to persist location {location_tuple}")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def persist_artist(artist_tuple: ArtistTuple) -> None:
        try:
            Persist.persist_artist_tuple(artist_tuple)
        except Exception as e:
            print(f"Unable to persist artist {artist_tuple.id}")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def persist_artist_hometown(artist_id: int, location_tuple: LocationTuple) -> None:
        try:
            _artist = Artist.query.filter_by(id=artist_id).first()
            _updated = location_tuple._replace(hometown_of=_artist)
            Persist.persist_location_tuple(_updated)
        except Exception as e:
            print(f"Unable to persist artist {artist_id} hometown {location_tuple}")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def delete_artist_birthplace(artist_uri: str) -> None:
        try:
            Persist.delete_birthplace(artist_uri)
        except Exception as e:
            print(f"Unable to delete artist {artist_id} birthplace")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def delete_artist_hometown(artist_uri: str) -> None:
        try:
            Persist.delete_hometown(artist_uri)
        except Exception as e:
            print(f"Unable to delete artist {artist_uri} hometown")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def persist_artist_birthplace(artist_id: int, location_tuple: LocationTuple) -> None:
        try:
            _artist = Artist.query.filter_by(id=artist_id).first()
            _updated = location_tuple._replace(birthplace_of=_artist)
            Persist.persist_location_tuple(_updated)
        except Exception as e:
            print(f"Unable to persist artist {artist_id} birthplace {location_tuple}")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def persist_lyrics(track_id: int, lyrics: Optional[str], url: str, fetched) -> None:
        _track = Track.query.filter_by(id=track_id).first()
        if lyrics:
            _updates = {Track.lyrics: lyrics, Track.lyrics_url: url, Track.lyrics_fetched_timestamp: fetched}
            try:
                Persist.update(Track, _track.id, _updates)
            except Exception as e:
                print(f"Unable to persist track lyrics {track_id}")
                traceback.print_tb(e.__traceback__)
                raise

    @staticmethod
    def persist_dbp_uri(model: db.Model, artist_id: int, dbp_uri: Optional[str]) -> None:
        _instance = model.query.filter_by(id=artist_id).first()
        if dbp_uri:
            _updates = {model.dbp_uri: dbp_uri}
            try:
                Persist.update(model, _instance.id, _updates)
            except Exception as e:
                print(f"Unable to persist {artist_id} dbp uri")
                traceback.print_tb(e.__traceback__)
                raise

    @staticmethod
    def persist_mb_metadata(model: db.Model, _id: int, _tuple) -> None:
        _entity = model.query.filter_by(id=_id).first()
        _updates = {model.mb_id: _tuple.id, model.mb_obj: _tuple._asdict()}
        try:
            Persist.update(model, _entity.id, _updates)

        except Exception as e:
            print(f"Unable to persist {_id} mb metadata")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def persist_lyrics_annotated(track_id: int, lyrics_annotated: AnnotationTuple) -> None:
        _track = Track.query.filter_by(id=track_id).first()
        _updates = {Track.lyrics_annotated: lyrics_annotated.text}
        try:
            Persist.update(Track, _track.id, _updates)
        except Exception as e:
            print(f"Unable to persist track {track_id} annotated lyrics")
            traceback.print_tb(e.__traceback__)
            raise

    @staticmethod
    def persist_lyrics_links(track_id: int, candidates: CandidatesTuple) -> None:
        _track = Track.query.filter_by(id=track_id).first()
        _updates = {Track.lyrics_annotations_json: candidates._asdict()}
        try:
            Persist.update(Track, _track.id, _updates)
        except Exception as e:
            print(f"Unable to persist track {track_id} annotations")
            traceback.print_tb(e.__traceback__)
            raise