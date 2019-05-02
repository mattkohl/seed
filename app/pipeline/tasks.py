from typing import Dict, List, Optional
from datetime import datetime
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
    def generate_lyrics_url(artists: List[str], title: str) -> str:
        return utils.GenUtils.link(artists, title)

    @staticmethod
    def get_lyrics(url) -> Optional[str]:
        return parser.GenParser.download(url)

    @staticmethod
    def persist_lyrics(track_id: int, lyrics: Optional[str], url: str, fetched) -> None:
        _track = Track.query.filter_by(id=track_id).first()
        if lyrics:
            Persist.update_track(_track.id, {Track.lyrics: lyrics, Track.lyrics_url: url, Track.lyrics_fetched: fetched})

    @staticmethod
    def run_playlist(playlist_uri) -> List[Dict]:
        playlist = Tasks.get_playlist_tracks(playlist_uri)
        track_dicts = Tasks.extract_tracks_from_playlist(playlist)
        track_tuples = Tasks.tuplify_tracks(track_dicts)
        [Tasks.persist_track(t) for t in track_tuples]
        track_dicts = [t._asdict() for t in track_tuples]
        return track_dicts

    @staticmethod
    def run_lyrics(track_uri: Optional[str] = None):
        tracks = [Track.query.filter_by(spot_uri=track_uri).first()] if track_uri is not None else Track.query.filter_by(lyrics=None).all()
        return [Tasks.run_lyric(t) for t in tracks]

    @staticmethod
    def run_lyric(track: Track):
        url = Tasks.generate_lyrics_url([_artist.name for _artist in track.artists], track.name)
        try:
            lyrics = Tasks.get_lyrics(url)
        except Exception as e:
            print(f"Could'nt connect to {url}: {e}")
        else:
            fetched = datetime.now()
            Tasks.persist_lyrics(track.id, lyrics, url, fetched)
            _track = track.as_dict()
            _track.update({"lyrics": lyrics, "lyrics_url": url, "lyrics_fetched": fetched})
            return _track
