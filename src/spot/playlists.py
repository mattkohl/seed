from typing import Dict, List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from src.spot.utils import SpotUtils


class PlaylistGrabber:

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def download(self, uri: str) -> Dict:
        username = uri.split(':')[2]
        playlist_id = uri.split(':')[4]
        return self.sp.user_playlist(username, playlist_id)

    def extract_tracks(self, uri: str) -> List[Dict]:
        playlist = self.download(uri)
        return [SpotUtils.extract_track(item["track"]) for item in playlist["tracks"]["items"]]


if __name__ == "__main__":
    from pprint import pprint
    test_uri = "spotify:user:matt.kohl-gb:playlist:2d1Q2cY735lRoXC8cC6DDJ"
    pg = PlaylistGrabber()
    pprint(pg.extract_tracks(test_uri))
