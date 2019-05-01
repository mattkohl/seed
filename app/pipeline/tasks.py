from typing import Dict, List, Optional

from flask import json

from app.geni import utils, parser
from app.models import Track
from app.persist.persist import Persist
from app.spot.models import TrackTuple
from app.spot.playlists import SpotPlaylist
from app.spot.utils import SpotUtils


class Tasks:

    @staticmethod
    def get_playlist_tracks(uri: str) -> Dict:
        sp = SpotPlaylist()
        return sp.download(uri)

    @staticmethod
    def extract_tracks_from_playlist(playlist: Dict) -> List[Dict]:
        return SpotUtils.extract_tracks(playlist)

    @staticmethod
    def tuplify_tracks(track_dicts: List[Dict]) -> List[TrackTuple]:
        return [Tasks.tuplify_track(track_dict) for track_dict in track_dicts]

    @staticmethod
    def tuplify_track(d: Dict) -> TrackTuple:
        _track = SpotUtils.extract_track(d)
        _album = _track.album._asdict()
        _artists = [_artist._asdict() for _artist in _track.artists]
        _updated = _track._replace(artists=_artists, album=_album)
        return _track

    @staticmethod
    def dump_track_tuple_to_json(track_tuple: TrackTuple):
        yield json.dumps(track_tuple._asdict(), indent=2, separators=(', ', ': '))

    @staticmethod
    def persist_track(track_tuple: TrackTuple) -> None:
        Persist.persist_track(track_tuple)

    @staticmethod
    def run(playlist_uri) -> List[Dict]:
        playlist = Tasks.get_playlist_tracks(playlist_uri)
        track_dicts = Tasks.extract_tracks_from_playlist(playlist)
        track_tuples = Tasks.tuplify_tracks(track_dicts)
        [Tasks.persist_track(t) for t in track_tuples]
        track_dicts = [t._asdict() for t in track_tuples]
        return track_dicts

    @staticmethod
    def get_lyrics(artists: List[str], title: str) -> Optional[str]:
        url = utils.GenUtils.link(artists, title)
        return parser.GenParser.download(url)

    @staticmethod
    def persist_lyrics(track_id: int, lyrics: str) -> None:
        _track = Track.query.filter_by(id=track_id).first
        Persist.update_track(_track, lyrics)

