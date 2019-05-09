from typing import Dict, List
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.spot.models import AlbumTuple
from app.spot.utils import SpotUtils


class SpotArtist:

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def download_albums(self, uri: str) -> List[Dict]:
        artist_id = uri.split(':')[-1]
        try:
            print(f"Downloaded artist {artist_id} albums")
            return self.sp.artist_albums(artist_id=artist_id, album_type="album", country="US", limit=50)["items"]
        except Exception as e:
            print(f"Unable to download artist {artist_id} albums: {e}")
            return list()

    @staticmethod
    def extract_albums(album_dicts: List[Dict]) -> List[AlbumTuple]:
        return [SpotUtils.extract_album(item) for item in album_dicts]
