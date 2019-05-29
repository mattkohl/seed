from typing import Dict, List

from app.models import Track
from app.tasks.fetch import Fetch
from app.tasks.persist import Persistence
from sqlalchemy.sql.expression import func


class Tasks:

    @staticmethod
    def run_playlist(playlist_uri) -> List[Dict]:
        track_tuples = Fetch.playlist_tracks(playlist_uri)
        [Persistence.persist_track(t) for t in track_tuples]
        return [t._asdict() for t in track_tuples]

    @staticmethod
    def run_random_track() -> Dict:
        _track = Track.query.filter(Track.lyrics == None).order_by(func.random()).first()
        return Tasks.run_track(_track.spot_uri)

    @staticmethod
    def run_track(track_uri) -> Dict:
        _ = Fetch.track(track_uri)
        _ = Fetch.track_dbp_uri(track_uri)
        _ = Fetch.track_lyrics(track_uri)
        _ = Fetch.track_lyrics_annotate(track_uri)
        return Fetch.track(track_uri)

    @staticmethod
    def run_artist(artist_uri) -> Dict:
        album_tuples = Fetch.artist_albums(artist_uri)
        [Persistence.persist_album(a) for a in album_tuples]
        _ = Fetch.artist_mb_metadata(artist_uri)
        _ = Fetch.artist_dbp_uri(artist_uri, True)
        _ = Fetch.artist_hometown(artist_uri)
        _ = Fetch.artist_birthplace(artist_uri)
        _ = Fetch.artist_spot_metadata(artist_uri)
        return Fetch.artist(artist_uri)

    @staticmethod
    def run_album(album_uri) -> Dict:
        track_tuples = Fetch.album_tracks(album_uri)
        [Persistence.persist_track(t) for t in track_tuples]
        _ = Fetch.album_dbp_uri(album_uri)
        _ = Fetch.album_mb_metadata(album_uri)
        return Fetch.album(album_uri)
