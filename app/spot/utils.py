from copy import deepcopy
from typing import Dict, List

from app.spot.models import AlbumTuple, ArtistTuple, TrackTuple


class SpotUtils:

    @staticmethod
    def extract_album(raw: Dict) -> AlbumTuple:
        """
        available keys:
            'album_type', 'artists', 'available_markets', 'external_urls',
            'href', 'id', 'images', 'name', 'release_date',
            'release_date_precision', 'total_tracks', 'type', 'uri'
        """
        raw.pop("available_markets")
        _raw = deepcopy(raw)
        _release_date = _raw["release_date"]
        _raw.update({"release_date": SpotUtils.clean_up_date(_release_date), "release_date_string": _release_date})
        return AlbumTuple(**_raw)

    @staticmethod
    def extract_artist(raw: Dict) -> ArtistTuple:
        """
        available keys:
            'external_urls', 'href', 'id', 'name', 'type', 'uri'
        """
        return ArtistTuple(**raw)

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
        _album = SpotUtils.extract_album(raw["album"])
        _artists = [SpotUtils.extract_artist(a) for a in raw["artists"]]

        _raw = deepcopy(raw)
        _raw.update({"album": _album, "artists": _artists})

        return TrackTuple(**_raw)

    @staticmethod
    def extract_tracks(track_items: Dict) -> List[TrackTuple]:
        return [track_item["track"] for track_item in track_items["tracks"]["items"]]

    @staticmethod
    def clean_up_date(raw_date):
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
