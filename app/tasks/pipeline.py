from typing import Dict, List

from app.models import Track, Album
from app.spot.utils import SpotUtils
from app.tasks.fetch import Fetch
from app.tasks.persist import TasksPersist
from app.spot.artists import SpotArtist


class Tasks:

    @staticmethod
    def run_playlist(playlist_uri) -> List[Dict]:
        playlist = Fetch.playlist_tracks(playlist_uri)
        track_dicts = SpotUtils.extract_tracks_from_playlist(playlist)
        track_tuples = SpotUtils.tuplify_tracks(track_dicts, None)
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
    def run_album_tracks(uri) -> List[Dict]:
        result = Album.query.filter_by(spot_uri=uri).first()
        track_dicts = Fetch.album_tracks(uri)
        track_tuples = SpotUtils.tuplify_tracks(track_dicts, result.as_album_tuple())
        [TasksPersist.persist_track(t) for t in track_tuples]
        _track_dicts = [t._asdict() for t in track_tuples]
        return track_dicts

    @staticmethod
    def scrape_all_lyrics() -> List[Dict]:
        return [Fetch.track_lyrics(_track.spot_uri) for _track in Track.query.filter_by(lyrics=None).all()]


