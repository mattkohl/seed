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
            a = self.sp.artist_albums(artist_id=artist_id, album_type="album", country="US", limit=50)
        except Exception as e:
            print(f"Unable to download artist {artist_id} albums: {e}")
            return list()
        else:
            print(f"Downloaded artist {artist_id} albums")
            return a

    def extract_albums(self, uri: str) -> List[AlbumTuple]:
        for item in self.sp.artist_albums(uri, "album", "US")["items"]:
            print(item)
            yield SpotUtils.extract_album(item)
