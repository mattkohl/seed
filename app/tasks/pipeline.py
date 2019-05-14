from typing import Dict, List

from app.tasks.fetch import Fetch
from app.tasks.persist import TasksPersist


class Tasks:

    @staticmethod
    def run_playlist(playlist_uri) -> List[Dict]:
        track_tuples = Fetch.playlist_tracks(playlist_uri)
        [TasksPersist.persist_track(t) for t in track_tuples]
        return [t._asdict() for t in track_tuples]

    @staticmethod
    def run_artist_albums(artist_uri) -> List[Dict]:
        album_tuples = Fetch.artist_albums(artist_uri)
        [TasksPersist.persist_album(a) for a in album_tuples]
        return [a._asdict() for a in album_tuples]

    @staticmethod
    def run_album_tracks(album_uri) -> List[Dict]:
        track_tuples = Fetch.album_tracks(album_uri)
        [TasksPersist.persist_track(t) for t in track_tuples]
        return [t._asdict() for t in track_tuples]
