import traceback

from src.spot.oauth2 import SpotifyClientCredentials
from src.spot.client import Spotify


class SpotAlbum:

    client_credentials_manager = SpotifyClientCredentials()
    sp = Spotify(client_credentials_manager=client_credentials_manager)

    def download_album(self, uri: str):
        album_id = uri.split(':')[-1]
        try:
            _album = self.sp.album(album_id)

        except Exception as e:
            print(f"Unable to download album {album_id}")
            traceback.print_tb(e.__traceback__)
            raise
        else:
            print(f"Downloaded album {album_id}")
            return _album
