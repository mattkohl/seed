from typing import Dict, List
import traceback

from app.spot.oauth2 import SpotifyClientCredentials
from app.spot.client import Spotify


class SpotArtist:

    client_credentials_manager = SpotifyClientCredentials()
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    def download_artist(self, uri: str) -> Dict:
        artist_id = uri.split(':')[-1]
        try:
            print(f"Downloading artist {artist_id}")
            return self.sp.artist(artist_id=artist_id)
        except Exception as e:
            print(f"Unable to download artist {artist_id}")
            traceback.print_tb(e.__traceback__)
            raise

    def download_artist_albums(self, uri: str) -> List[Dict]:
        artist_id = uri.split(':')[-1]
        try:
            print(f"Downloading artist {artist_id} albums")
            return self.sp.artist_albums(artist_id=artist_id, album_type="album", country="US", limit=50)["items"]
        except Exception as e:
            print(f"Unable to download artist {artist_id} albums")
            traceback.print_tb(e.__traceback__)
            raise
