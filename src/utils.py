from typing import Dict, List


class SpotifyUtils:

    @staticmethod
    def extract_album(raw: Dict) -> Dict:
        """
        available keys: 'album_type', 'artists', 'available_markets', 'external_urls', 'href', 'id', 'images', 'name', 'release_date', 'release_date_precision', 'total_tracks', 'type', 'uri'
        """
        return {"title": raw["name"], "release_date": raw["release_date"], "uri": raw["uri"]}

    @staticmethod
    def extract_artist(raw: Dict) -> Dict:
        """
        available keys: 'external_urls', 'href', 'id', 'name', 'type', 'uri'
        """
        return {"name": raw["name"], "uri": raw["uri"]}

    @staticmethod
    def extract_track(raw: Dict) -> Dict:
        """
        available keys: 'album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'episode', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track', 'track_number', 'type', 'uri'
        """
        return {
            "title": raw["name"],
            "uri": raw["uri"],
            "popularity": raw["popularity"],
            "album": SpotifyUtils.extract_album(raw["album"]),
            "artists": [SpotifyUtils.extract_artist(a) for a in raw["artists"]]
        }