from typing import Dict
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotPlaylist:

    client_credentials_manager = SpotifyClientCredentials()
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def download_tracks(self, uri: str) -> Dict:
        username = uri.split(':')[2]
        playlist_id = uri.split(':')[4]
        try:
            pl = self.sp.user_playlist(username, playlist_id)
        except Exception as e:
            print(f"Unable to download playlist {playlist_id}:", e)
            raise
        else:
            print(f"Downloaded playlist {playlist_id}")
            return pl
