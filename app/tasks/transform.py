from typing import Dict, List

from app.spot.models import TrackTuple
from app.spot.utils import SpotUtils


class TasksTransform:

    @staticmethod
    def extract_tracks_from_playlist(playlist: Dict) -> List[Dict]:
        return SpotUtils.extract_tracks_from_playlist(playlist)

    @staticmethod
    def extract_tracks_from_album(album: Dict) -> List[Dict]:
        return SpotUtils.extract_tracks_from_album(album)

    @staticmethod
    def tuplify_tracks(track_dicts: List[Dict]) -> List[TrackTuple]:
        return [TasksTransform.tuplify_track(track_dict) for track_dict in track_dicts]

    @staticmethod
    def tuplify_track(d: Dict) -> TrackTuple:
        _track = SpotUtils.extract_track(d)
        _album = _track.album._asdict()
        _artists = [_artist._asdict() for _artist in _track.artists]
        _updated = _track._replace(artists=_artists, album=_album)
        return _track

