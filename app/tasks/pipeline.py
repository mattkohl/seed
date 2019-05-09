from typing import Dict, List

from app.models import Track
from app.tasks.fetch import Fetch
from app.tasks.persist import TasksPersist
from app.spot.artists import SpotArtist
from app.tasks.transform import TasksTransform


class Tasks:

    @staticmethod
    def run_playlist(playlist_uri) -> List[Dict]:
        playlist = Fetch.playlist_tracks(playlist_uri)
        track_dicts = TasksTransform.extract_tracks_from_playlist(playlist)
        track_tuples = TasksTransform.tuplify_tracks(track_dicts)
        [TasksPersist.persist_track(t) for t in track_tuples]
        _track_dicts = [t._asdict() for t in track_tuples]
        return _track_dicts

    @staticmethod
    def run_artist_albums(artist_uri) -> List[Dict]:
        sp = SpotArtist()
        album_dicts = sp.download_albums(artist_uri)
        album_tuples = sp.extract_albums(album_dicts)
        [TasksPersist.persist_album(a) for a in album_tuples]
        return [a._asdict() for a in album_tuples]

    @staticmethod
    def run_album_tracks(album_uri) -> List[Dict]:
        _album = Fetch.album_tracks(album_uri)
        print(_album)
        # track_dicts = TasksTransform.extract_tracks_from_album(_album)
        # track_tuples = TasksTransform.tuplify_tracks(track_dicts)
        # [TasksPersist.persist_track(t) for t in track_tuples]
        # _track_dicts = [t._asdict() for t in track_tuples]
        return _album

    @staticmethod
    def scrape_all_lyrics() -> List[Dict]:
        return [Fetch.track_lyrics(_track.spot_uri) for _track in Track.query.filter_by(lyrics=None).all()]


