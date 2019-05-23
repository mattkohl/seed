from typing import Optional
import traceback

from app import db
from app.dbp.models import CandidatesTuple, AnnotationTuple
from app.mb.models import MbArtistTuple as MBArtistTuple
from app.models import Track, Artist, Album
from app.persist.persist import Persist
from app.spot.models import TrackTuple, AlbumTuple


class Persistence:

    @staticmethod
    def clear():
        message = f"Deleted {Track.query.count()} Tracks, {Artist.query.count()} Artists, & {Album.query.count()} Albums"
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
