from typing import Dict, List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class PlaylistGrabber:

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def download(self, uri: str) -> Dict:
        username = uri.split(':')[2]
        playlist_id = uri.split(':')[4]
        results = self.sp.user_playlist(username, playlist_id)
        return results

    def extract_tracks(self, uri: str) -> List[Dict]:
        playlist = self.download(uri)
        return [self.extract_track(item["track"]) for item in playlist["tracks"]["items"]]

    def extract_track(self, raw: Dict) -> Dict:
        """
        available keys: 'album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'episode', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track', 'track_number', 'type', 'uri'
        """
        return {
            "title": raw["name"],
            "uri": raw["uri"],
            "popularity": raw["popularity"],
            "album": self.extract_album(raw["album"]),
            "artists": [self.extract_artist(a) for a in raw["artists"]]
        }

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


if __name__ == "__main__":
    import pprint
    hh = "spotify:user:matt.kohl-gb:playlist:2d1Q2cY735lRoXC8cC6DDJ"
    pg = PlaylistGrabber()
    pprint.pprint(pg.extract_tracks(hh))
