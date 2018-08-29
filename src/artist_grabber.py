from typing import Dict, List

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class ArtistGrabber:

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def download(self, name: str) -> List[Dict]:
        _results = self.sp.search(q=name, limit=20, type="artist")
        return [self.extract(result) for result in _results["artists"]["items"][:1]]

    @staticmethod
    def extract(raw: Dict) -> Dict:
        """
        available keys: 'external_urls', 'followers', 'genres', 'href', 'id', 'images', 'name', 'popularity', 'type', 'uri'
        """
        return {
            "name": raw["name"],
            "uri": raw["uri"],
            "external_urls": raw["external_urls"],
            "popularity": raw["popularity"],
            "genres": raw["genres"]
        }


if __name__ == "__main__":
    from pprint import pprint
    ag = ArtistGrabber()
    test = "gang starr"
    results = ag.download(test)
    for r in results:
        pprint(r)
