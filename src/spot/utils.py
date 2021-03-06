import traceback
from copy import deepcopy
from typing import Dict, List, Optional

from src.spot.models import AlbumTuple, ArtistTuple, TrackTuple, GenreTuple


class SpotUtils:

    @staticmethod
    def extract_album(raw: Dict) -> Optional[AlbumTuple]:
        raw.pop("available_markets", None)
        _raw = deepcopy(raw)
        _release_date = _raw["release_date"]
        _release_date_string = _raw["release_date_string"] if "release_date_string" in _raw else _release_date
        try:
            _artists = [SpotUtils.extract_artist(a) for a in raw["artists"]]
            _raw.update({"artists": _artists, "release_date": SpotUtils.clean_up_date(_release_date), "release_date_string": _release_date_string})
            _album_tuple = AlbumTuple(**_raw)
        except Exception as e:
            print(f"Exception when trying to extract album")
            print(raw)
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return _album_tuple

    @staticmethod
    def extract_albums(album_dicts: List[Dict]) -> List[AlbumTuple]:
        return [SpotUtils.extract_album(item) for item in album_dicts]

    @staticmethod
    def extract_artist(raw: Dict) -> Optional[ArtistTuple]:
        _raw = deepcopy(raw)
        try:
            _genres = SpotUtils.extract_genres(_raw['genres']) if 'genres' in _raw else list()
            _raw.update({"genres": _genres})
            _artist_tuple = ArtistTuple(**_raw)
        except Exception as e:
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return _artist_tuple

    @staticmethod
    def extract_genres(raw: List[str]) -> List[GenreTuple]:
        return [GenreTuple(name=g.replace(" ", "-").lower()) for g in raw]

    @staticmethod
    def extract_track(raw: Dict) -> TrackTuple:
        """
        available keys:
            'album', 'artists', 'available_markets', 'disc_number',
            'duration_ms', 'episode', 'explicit', 'external_ids',
            'external_urls', 'href', 'id', 'is_local', 'name',
            'popularity', 'preview_url', 'track', 'track_number', 'type', 'uri'
        """
        try:
            raw.pop("available_markets", None)
            _raw = deepcopy(raw)
            _album = SpotUtils.extract_album(_raw["album"])
            _primary_artists = _album.artists
            _primary_artists_names = [_pa.name for _pa in _primary_artists]
            _featured_artists_raw = [SpotUtils.extract_artist(a) for a in _raw["artists"]]
            _featured_artists = [_fa for _fa in _featured_artists_raw if _fa.name not in _primary_artists_names]
            _raw.pop("artists")
            _raw.update({"album": _album, "primary_artists": _primary_artists, "featured_artists": _featured_artists})
        except Exception as e:
            print(f"Exception when trying to extract track")
            print(raw)
            traceback.print_tb(e.__traceback__)
            raise
        else:
            return TrackTuple(**_raw)

    @staticmethod
    def extract_tracks_from_playlist(track_items: List[Dict]) -> List[Dict]:
        return [track_item["track"] for track_item in track_items]

    @staticmethod
    def tuplify_tracks(track_dicts: List[Dict]) -> List[TrackTuple]:
        return [SpotUtils.tuplify_track(track_dict) for track_dict in track_dicts if track_dict is not None]

    @staticmethod
    def tuplify_track(d: Dict) -> Optional[TrackTuple]:
        try:
            _track = SpotUtils.extract_track(d)
        except Exception as e:
            print(f"Unable to tuplify track")
            print(d)
            traceback.print_tb(e.__traceback__)
            return None
        else:
            return _track

    @staticmethod
    def clean_up_date(raw_date) -> str:
        new_date = raw_date
        month = new_date[-2:]
        if len(new_date) == 7 and month == '02':
            return new_date + '-28'
        if len(new_date) == 7 and month in ['04', '06', '11', '09']:
            return new_date + '-30'
        if len(new_date) == 7:
            return new_date + '-31'
        if len(new_date) == 4:
            return new_date + '-12-31'
        return new_date
