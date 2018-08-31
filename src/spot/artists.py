from typing import Dict, List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from src.spot.utils import SpotUtils


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

    def albums(self, uri: str) -> List[Dict]:
        return [SpotUtils.extract_album(a) for a in self.sp.artist_albums(uri, "album", "US")["items"]]


if __name__ == "__main__":
    from pprint import pprint
    test_uri = "spotify:artist:13ubrt8QOOCPljQ2FL1Kca"
    sa = SpotArtist()
    pprint(sa.albums(test_uri))
