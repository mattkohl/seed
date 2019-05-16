import traceback
from copy import deepcopy
from typing import Dict, List, Optional

from app.spot.models import AlbumTuple, ArtistTuple, TrackTuple


class SpotUtils:

    @staticmethod
    def extract_album(raw: Dict) -> Optional[AlbumTuple]:
        """
        available keys:
            'album_type', 'artists', 'available_markets', 'external_urls',
            'href', 'id', 'images', 'name', 'release_date',
            'release_date_precision', 'total_tracks', 'type', 'uri'
        """
        if "available_markets" in raw:
            raw.pop("available_markets")
        _raw = deepcopy(raw)
        _release_date = _raw["release_date"]
        try:
            _artists = [SpotUtils.extract_artist(a) for a in raw["artists"]]
            _raw.update({"artists": _artists, "release_date": SpotUtils.clean_up_date(_release_date), "release_date_string": _release_date})
            _album_tuple = AlbumTuple(**_raw)
        except Exception:
            print(f"Exception when trying to extract album")
            print(raw)
            raise
        else:
            return _album_tuple

    @staticmethod
    def extract_albums(album_dicts: List[Dict]) -> List[AlbumTuple]:
        return [SpotUtils.extract_album(item) for item in album_dicts]

    @staticmethod
    def extract_artist(raw: Dict) -> Optional[ArtistTuple]:
        """
        available keys:
            'external_urls', 'href', 'id', 'name', 'type', 'uri'
        """
        try:
            _artist_tuple = ArtistTuple(**raw)
        except Exception:
            raise
        else:
            return _artist_tuple

    @staticmethod
    def extract_track(raw: Dict) -> TrackTuple:
        """
        available keys:
            'album', 'artists', 'available_markets', 'disc_number',
            'duration_ms', 'episode', 'explicit', 'external_ids',
            'external_urls', 'href', 'id', 'is_local', 'name',
            'popularity', 'preview_url', 'track', 'track_number', 'type', 'uri'
        """
        raw.pop("available_markets")
        _raw = deepcopy(raw)
        _album = SpotUtils.extract_album(raw["album"])
        _artists = [SpotUtils.extract_artist(a) for a in raw["artists"]]
        _raw.update({"album": _album, "artists": _artists})
        return TrackTuple(**_raw)

    @staticmethod
    def extract_tracks_from_playlist(track_items: List[Dict]) -> List[Dict]:
        return [track_item["track"] for track_item in track_items]

    @staticmethod
    def tuplify_tracks(track_dicts: List[Dict], album: Optional[AlbumTuple]) -> List[TrackTuple]:
        return [SpotUtils.tuplify_track(track_dict, album) for track_dict in track_dicts if track_dict is not None]

    @staticmethod
    def tuplify_track(d: Dict, album: Optional[AlbumTuple]) -> Optional[TrackTuple]:
        try:
            if album:
                d.update({"album": album._asdict()})
            _track = SpotUtils.extract_track(d)
            _album = _track.album._asdict()
            _artists = [_artist._asdict() for _artist in _track.artists]
            _updated = _track._replace(artists=_artists, album=_album)
        except Exception as e:
            print(f"Unable to tuplify track")
            print(f"track_dict: {d}")
            print(f"album: {album}")
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
