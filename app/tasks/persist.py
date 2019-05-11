from typing import Optional

from app.dbp.models import CandidatesTuple, AnnotationTuple
from app.mb.models import ArtistTuple as MBArtistTuple
from app.models import Track, Artist
from app.persist.persist import Persist
from app.spot.models import TrackTuple, AlbumTuple


class TasksPersist:

    @staticmethod
    def persist_track(track_tuple: TrackTuple) -> None:
        Persist.persist_track_tuple(track_tuple)

    @staticmethod
    def persist_album(album_tuple: AlbumTuple) -> None:
        Persist.persist_album_tuple(album_tuple)

    @staticmethod
    def persist_lyrics(track_id: int, lyrics: Optional[str], url: str, fetched) -> None:
        _track = Track.query.filter_by(id=track_id).first()
        if lyrics:
            _updates = {Track.lyrics: lyrics, Track.lyrics_url: url, Track.lyrics_fetched_timestamp: fetched}
            Persist.update_track(_track.id, _updates)

    @staticmethod
    def persist_dbp_uri(artist_id: int, dbp_uri: Optional[str]) -> None:
        _artist = Track.query.filter_by(id=artist_id).first()
        if dbp_uri:
            _updates = {Artist.dbp_uri: dbp_uri}
            Persist.update(Artist, _artist.id, _updates)

    @staticmethod
    def persist_mb_metadata(artist_id: int, artist_tuple: MBArtistTuple) -> None:
        _artist = Track.query.filter_by(id=artist_id).first()
        _updates = {Artist.mb_id: artist_tuple.id, Artist.mb_obj: artist_tuple._asdict()}
        Persist.update(Artist, _artist.id, _updates)

    @staticmethod
    def persist_lyrics_annotated(track_id: int, lyrics_annotated: AnnotationTuple) -> None:
        _track = Track.query.filter_by(id=track_id).first()
        _updates = {Track.lyrics_annotated: lyrics_annotated.text}
        Persist.update_track(_track.id, _updates)

    @staticmethod
    def persist_lyrics_links(track_id: int, candidates: CandidatesTuple) -> None:
        _track = Track.query.filter_by(id=track_id).first()
        _updates = {Track.lyrics_annotations_json: candidates._asdict()}
        Persist.update_track(_track.id, _updates)
