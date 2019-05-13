from typing import Dict, List

from app.models import Track, Album
from app.spot.utils import SpotUtils
from app.tasks.fetch import Fetch
from app.tasks.persist import TasksPersist
import traceback


class Tasks:

    @staticmethod
    def run_playlist(playlist_uri) -> List[Dict]:
        track_tuples = Fetch.playlist_tracks(playlist_uri)
        [TasksPersist.persist_track(t) for t in track_tuples]
        return [t._asdict() for t in track_tuples]

    @staticmethod
    def run_artist_albums(artist_uri) -> List[Dict]:
        try:
            album_tuples = Fetch.artist_albums(artist_uri)
            [TasksPersist.persist_album(a) for a in album_tuples]
        except Exception as e:
            print(f"Unable to retrieve albums for artist {artist_uri}:", traceback.print_tb(e.__traceback__))
            raise
        else:
            return [a._asdict() for a in album_tuples]

    @staticmethod
    def run_album_tracks(album_uri) -> List[Dict]:
        try:
            result = Album.query.filter_by(spot_uri=album_uri).first()
            track_dicts = Fetch.album_tracks(album_uri)
            track_tuples = SpotUtils.tuplify_tracks(track_dicts, result.as_album_tuple())
            [TasksPersist.persist_track(t) for t in track_tuples]
            _track_dicts = [t._asdict() for t in track_tuples]

        return track_dicts
