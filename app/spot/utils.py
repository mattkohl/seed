from copy import deepcopy
from typing import Dict

from app.spot.models import Album, Artist, Track


class SpotUtils:

    @staticmethod
    def extract_album(raw: Dict) -> Album:
        """
        available keys:
            'album_type', 'artists', 'available_markets', 'external_urls',
            'href', 'id', 'images', 'name', 'release_date',
            'release_date_precision', 'total_tracks', 'type', 'uri'
        """
        raw.pop("available_markets")
        return Album(**raw)

    @staticmethod
    def extract_artist(raw: Dict) -> Artist:
        """
        available keys:
            'external_urls', 'href', 'id', 'name', 'type', 'uri'
        """
        return Artist(**raw)

    @staticmethod
    def extract_track(raw: Dict) -> Track:
        """
        available keys:
            'album', 'artists', 'available_markets', 'disc_number',
            'duration_ms', 'episode', 'explicit', 'external_ids',
            'external_urls', 'href', 'id', 'is_local', 'name',
            'popularity', 'preview_url', 'track', 'track_number', 'type', 'uri'
        """
        raw.pop("available_markets")
        album = SpotUtils.extract_album(raw["album"])
        artists = [SpotUtils.extract_artist(a) for a in raw["artists"]]

        _raw = deepcopy(raw)
        _raw.update({"album": album, "artists": artists})

        return Track(**_raw)
