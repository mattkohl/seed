from typing import Dict
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotAlbum:

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def download_tracks(self, uri: str) -> Dict:
        album_id = uri.split(':')[-1]
        try:
            album_dict = self.sp.album_tracks(album_id)
        except Exception as e:
            print(f"Unable to download tracks for {album_id}:", e)
            raise
        else:
            print(f"Downloaded playlist {album_id}")
            return album_dict
