import traceback
from typing import Dict, List

from app.spot.oauth2 import SpotifyClientCredentials
from app.spot.client import Spotify


class SpotAlbum:

    client_credentials_manager = SpotifyClientCredentials()
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    def download_album_tracks(self, uri: str) -> List[Dict]:
        album_id = uri.split(':')[-1]
        try:
            track_dicts = self.sp.album_tracks(album_id)["items"]
        except Exception as e:
            print(f"Unable to download tracks for {album_id}")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            print(f"Downloaded playlist {album_id}")
            return track_dicts
