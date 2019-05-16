from typing import Dict, List

from app.tasks.fetch import Fetch
from app.tasks.persist import Persistence


class Tasks:

    @staticmethod
    def run_playlist(playlist_uri) -> List[Dict]:
        track_tuples = Fetch.playlist_tracks(playlist_uri)
        [Persistence.persist_track(t) for t in track_tuples]
        return [t._asdict() for t in track_tuples]

    @staticmethod
    def run_track(track_uri) -> Dict:
        _ = Fetch.track(track_uri)
        _ = Fetch.track_dbp_uri(track_uri)
        _ = Fetch.track_lyrics(track_uri)
        _ = Fetch.lyrics_annotate(track_uri)
        return Fetch.track(track_uri)

    @staticmethod
    def run_artist(artist_uri) -> Dict:
        album_tuples = Fetch.artist_albums(artist_uri)
        [Persistence.persist_album(a) for a in album_tuples]
        _ = Fetch.artist_mb_metadata(artist_uri)
        _ = Fetch.artist_dbp_uri(artist_uri)
        return Fetch.artist(artist_uri)

    @staticmethod
    def run_album(album_uri) -> Dict:
        track_tuples = Fetch.album_tracks(album_uri)
        [Persistence.persist_track(t) for t in track_tuples]
        _ = Fetch.album_dbp_uri(album_uri)
        return Fetch.album(album_uri)
