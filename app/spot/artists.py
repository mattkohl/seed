from typing import Dict, List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.spot.models import Album
from app.spot.utils import SpotUtils


class SpotArtist:

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def search(self, name: str) -> List[Dict]:
        """
        available keys: 'external_urls', 'followers', 'genres', 'href', 'id', 'images', 'name', 'popularity', 'type', 'uri'
        """
        return self.sp.search(q=name, limit=20, type="artist")

    def download(self, uri: str) -> Dict:
        return self.sp.artist(uri)

    def extract_albums(self, uri: str) -> List[Album]:
        for item in self.sp.artist_albums(uri, "album", "US")["items"]:
            print(item)
            yield SpotUtils.extract_album(item)
